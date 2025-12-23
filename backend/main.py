import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from dotenv import load_dotenv
import hashlib
import cohere
import logging
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not all([QDRANT_HOST, QDRANT_API_KEY, COHERE_API_KEY]):
    logging.error("Missing one or more environment variables: QDRANT_HOST, QDRANT_API_KEY, COHERE_API_KEY")
    raise ValueError("Missing one or more environment variables: QDRANT_HOST, QDRANT_API_KEY, COHERE_API_KEY")

# Initialize Cohere Client
try:
    co = cohere.Client(COHERE_API_KEY)
except cohere.CohereError as e:
    logging.error(f"Failed to initialize Cohere client: {e}")
    raise ValueError(f"Failed to initialize Cohere client: {e}")

# For testing purposes, log the loaded keys (REMOVE IN PRODUCTION)
logging.info(f"QDRANT_HOST: {QDRANT_HOST}")
logging.info(f"QDRANT_API_KEY: {'*' * len(QDRANT_API_KEY) if QDRANT_API_KEY else None}")
logging.info(f"COHERE_API_KEY: {'*' * len(COHERE_API_KEY) if COHERE_API_KEY else None}")

# Ensure python-dotenv is in requirements.txt
# (It might not be strictly necessary for production if env vars are set externally,
# but good for local development and explicit loading)

def get_all_urls(base_url: str) -> set[str]:
    """
    Crawls the Docusaurus site and extracts all public content URLs.
    """
    visited_urls = set()
    urls_to_visit = {base_url}
    base_domain = urlparse(base_url).netloc

    while urls_to_visit:
        current_url = urls_to_visit.pop()
        if current_url in visited_urls:
            continue

        logging.info(f"Crawling: {current_url}")
        visited_urls.add(current_url)

        try:
            response = requests.get(current_url, timeout=10)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all links
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                absolute_url = urljoin(current_url, href)
                parsed_absolute_url = urlparse(absolute_url)

                # Ensure it's an HTTP/HTTPS URL and within the same domain
                if parsed_absolute_url.scheme in ['http', 'https'] and parsed_absolute_url.netloc == base_domain:
                    # Ignore anchor links within the same page, and common non-content paths
                    if '#' in absolute_url:
                        absolute_url = absolute_url.split('#')[0]
                    if not (absolute_url.endswith('.pdf') or 
                            absolute_url.endswith('.png') or
                            absolute_url.endswith('.jpg') or
                            absolute_url.endswith('.jpeg') or
                            '/api/' in absolute_url or # Example: ignore API docs if any
                            '/blog/' in absolute_url): # Example: ignore blog if any
                        
                        if absolute_url not in visited_urls:
                            urls_to_visit.add(absolute_url)
        except requests.exceptions.RequestException as e:
            logging.warning(f"Error crawling {current_url}: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred for {current_url}: {e}")
            
    # Filter out non-content URLs if specific patterns are known for Docusaurus content pages
    # For Docusaurus, content typically resides under /docs/
    # This example assumes general content discovery, further refinement might be needed
    content_urls = {url for url in visited_urls if "/docs/" in url or url == base_url}
    
    return content_urls

def extract_text_from_url(url: str) -> tuple[str, str]:
    """
    Fetches content from a URL, parses HTML, and extracts clean textual content.
    Returns a tuple of (page_title, clean_text).
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title
        page_title = soup.title.string if soup.title else url

        # Remove elements that are typically not part of the main content
        for unwanted_tag in ['nav', 'footer', 'aside', 'script', 'style', 'header', '.navbar', '.theme-doc-sidebar-container', '.pagination-nav', '.docs-navigation']:
            for tag in soup.find_all(unwanted_tag):
                tag.decompose()

        # Try to find the main content area. This might need refinement for specific Docusaurus themes.
        # Common patterns: <main>, <article>, <div> with specific classes like .docItemContainer, .markdown
        main_content = soup.find('main') or soup.find('article') or soup.find(class_='docItemContainer') or soup.find(class_='markdown')

        if main_content:
            clean_text = main_content.get_text(separator='\n', strip=True)
        else:
            # Fallback if specific content area is not found
            clean_text = soup.get_text(separator='\n', strip=True)

        # Basic cleanup: remove excessive newlines and spaces
        clean_text = os.linesep.join([s for s in clean_text.splitlines() if s.strip()])
        
        return page_title, clean_text

    except requests.exceptions.RequestException as e:
        logging.warning(f"Error fetching or processing {url}: {e}")
        return url, ""
    except Exception as e:
        logging.error(f"An unexpected error occurred for {url}: {e}")
        return url, ""

def chunk_text(documents: list[dict], chunk_size: int = 1000, chunk_overlap: int = 200) -> list[dict]:
    """
    Splits extracted text into configurable-sized chunks and generates metadata.
    """
    chunked_documents = []
    
    for doc in tqdm(documents, desc="Chunking documents"):
        text = doc["text"]
        url = doc["url"]
        title = doc["title"]
        
        # Simple character-based chunking
        start = 0
        chunk_index = 0
        while start < len(text):
            end = start + chunk_size
            chunk_content = text[start:end]
            
            # Generate content hash
            content_hash = hashlib.sha256(chunk_content.encode('utf-8')).hexdigest()
            
            chunked_documents.append({
                "chunk_text": chunk_content,
                "source_url": url,
                "page_title": title,
                "chunk_index": chunk_index,
                "content_hash": content_hash
            })
            
            start += chunk_size - chunk_overlap
            chunk_index += 1
            
    logging.info(f"Original documents: {len(documents)}, Chunked documents: {len(chunked_documents)}")
    return chunked_documents

def embed_chunks(chunked_documents: list[dict], model: str = "embed-english-v3.0") -> list[dict]:
    """
    Generates embeddings for text chunks using the Cohere API.
    """
    texts_to_embed = [doc["chunk_text"] for doc in chunked_documents]
    
    try:
        # Cohere API supports batch embedding
        response = co.embed(
            texts=texts_to_embed,
            model=model,
            input_type="classification" # or "clustering", "search_query", "search_document"
        )
        
        embeddings = response.embeddings
        
        # Attach embeddings to the corresponding chunks
        for i, embedding in enumerate(embeddings):
            chunked_documents[i]["embedding"] = embedding
            
        logging.info(f"Generated embeddings for {len(embeddings)} chunks.")
        return chunked_documents
        
    except cohere.CohereError as e:
        logging.error(f"Error generating embeddings with Cohere API: {e}")
        return []
    except Exception as e:
        logging.error(f"An unexpected error occurred during embedding: {e}")
        return []

from qdrant_client import QdrantClient, models

def create_qdrant_collection(collection_name: str, vector_size: int, distance: models.Distance):
    """
    Ensures the Qdrant collection exists with the specified configuration.
    """
    client = QdrantClient(url=QDRANT_HOST, api_key=QDRANT_API_KEY)
    
    try:
        # Check if collection exists
        if not client.collection_exists(collection_name=collection_name):
            logging.info(f"Creating Qdrant collection '{collection_name}'...")
            client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(size=vector_size, distance=distance),
                # Add any other payload schema definitions here if needed for indexing
                # For now, we'll store all metadata in payload without strict schema
            )
            logging.info(f"Collection '{collection_name}' created successfully.")
        else:
            logging.info(f"Collection '{collection_name}' already exists.")
            
    except Exception as e:
        logging.error(f"Error managing Qdrant collection '{collection_name}': {e}")
        raise

def save_chunks_to_qdrant(collection_name: str, chunked_documents: list[dict]):
    """
    Stores chunked documents with their embeddings and metadata into Qdrant.
    """
    client = QdrantClient(url=QDRANT_HOST, api_key=QDRANT_API_KEY)

    points = []
    for i, doc in enumerate(chunked_documents):
        # Qdrant expects payload as a dictionary
        payload = {
            "chunk_text": doc["chunk_text"],
            "source_url": doc["source_url"],
            "page_title": doc["page_title"],
            "chunk_index": doc["chunk_index"],
            "content_hash": doc["content_hash"],
        }
        
        # Ensure embedding exists
        if "embedding" not in doc or not doc["embedding"]:
            logging.warning(f"Skipping point {i} due to missing embedding.")
            continue

        points.append(
            models.PointStruct(
                id=i,  # Simple incremental ID for now; consider UUIDs for production
                vector=doc["embedding"],
                payload=payload
            )
        )
    
    if not points:
        logging.info("No points to save to Qdrant.")
        return

    try:
        operation_info = client.upsert(
            collection_name=collection_name,
            wait=True,
            points=points
        )
        logging.info(f"Saved {len(points)} chunks to Qdrant. Operation info: {operation_info}")
    except Exception as e:
        logging.error(f"Error saving chunks to Qdrant: {e}")
        raise


BASE_URL = "https://hackathon1-44os.vercel.app/"

def main():
    logging.info(f"Starting RAG ingestion pipeline for {BASE_URL}")
    
    # T006 [US1]: Integrate get_all_urls and extract_text_from_url
    content_urls = get_all_urls(BASE_URL)
    logging.info(f"Found {len(content_urls)} content URLs.")
    
    documents = []
    for url in tqdm(content_urls, desc="Extracting text from URLs"):
        page_title, clean_text = extract_text_from_url(url)
        if clean_text:
            documents.append({"url": url, "title": page_title, "text": clean_text})
        else:
            logging.warning(f"Skipping {url} due to empty content.")
            
    logging.info(f"Extracted content from {len(documents)} raw documents.")

    # T007 [US1]: Implement chunk_text function
    chunked_documents = chunk_text(documents)
    logging.info(f"Generated {len(chunked_documents)} chunks.")

    # T008 [US1]: Implement embed_chunks function
    chunked_documents_with_embeddings = embed_chunks(chunked_documents)
    if not chunked_documents_with_embeddings:
        logging.error("No embeddings generated, stopping ingestion.")
        return

    # T009 [US1]: Implement create_qdrant_collection function
    COLLECTION_NAME = "rag_embedding"
    # Assuming Cohere embed-english-v3.0 has 1024 dimensions
    # It's good practice to get this dynamically from the model or verify
    VECTOR_SIZE = 1024 
    create_qdrant_collection(COLLECTION_NAME, VECTOR_SIZE, models.Distance.COSINE)

    # T010 [US1]: Implement save_chunks_to_qdrant function
    # T012: Implement logic to detect content changes (using content_hash) and update only modified content in Qdrant (FR-009)
    # This requires more advanced logic to:
    # 1. Query Qdrant for existing points by source_url and content_hash.
    # 2. Compare new chunks with existing ones to identify additions, modifications, and deletions.
    # 3. Perform targeted upserts for new/modified chunks and deletions for removed chunks.
    # For now, the save_chunks_to_qdrant function will upsert all provided chunks.
    save_chunks_to_qdrant(COLLECTION_NAME, chunked_documents_with_embeddings)
    logging.info("RAG ingestion pipeline completed.")

    # T014: Minimal validation step
    try:
        client = QdrantClient(url=QDRANT_HOST, api_key=QDRANT_API_KEY)
        collection_info = client.get_collection(collection_name=COLLECTION_NAME)
        if collection_info.points_count > 0:
            logging.info(f"Validation: Qdrant collection '{COLLECTION_NAME}' contains {collection_info.points_count} points. Ingestion appears successful.")
        else:
            logging.warning(f"Validation: Qdrant collection '{COLLECTION_NAME}' is empty. Ingestion might have failed or no content was processed.")
    except Exception as e:
        logging.error(f"Validation failed: Could not connect to Qdrant or get collection info: {e}")

if __name__ == "__main__":
    main()