# backend/validator.py
import os
import json
import logging
import argparse
from tqdm import tqdm
from retriever import query_to_embedding, search_qdrant # Import retrieval functions

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_validation_dataset(filepath: str) -> list[dict]:
    """
    Loads a predefined dataset of test queries and their corresponding expected relevant document chunks.
    Dataset format:
    [
        {"query": "What is Docusaurus?", "expected_urls": ["https://.../docs/intro"], "expected_content_hashes": ["hash1", "hash2"]},
        ...
    ]
    """
    if not os.path.exists(filepath):
        logging.error(f"Validation dataset file not found: {filepath}")
        return []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    logging.info(f"Loaded {len(dataset)} validation queries from {filepath}")
    return dataset

def evaluate_retrieval(dataset: list[dict], top_k: int = 5) -> dict:
    """
    Executes retrievals for each query in the dataset and stores the retrieved results.
    """
    results = []
    for entry in tqdm(dataset, desc="Evaluating retrievals"):
        query = entry["query"]
        expected_urls = entry.get("expected_urls", [])
        expected_content_hashes = entry.get("expected_content_hashes", [])

        try:
            query_emb = query_to_embedding(query)
            retrieved_chunks = search_qdrant(query_emb, top_k=top_k)
            
            results.append({
                "query": query,
                "expected_urls": expected_urls,
                "expected_content_hashes": expected_content_hashes,
                "retrieved_chunks": retrieved_chunks
            })
        except Exception as e:
            logging.error(f"Error during retrieval for query '{query}': {e}")
            results.append({
                "query": query,
                "expected_urls": expected_urls,
                "expected_content_hashes": expected_content_hashes,
                "retrieved_chunks": [],
                "error": str(e)
            })
    return results

def calculate_accuracy_metrics(evaluation_results: list[dict], top_k: int = 5) -> dict:
    """
    Calculates quantitative measures of retrieval accuracy (e.g., precision@k, recall@k, MRR).
    """
    total_queries = len(evaluation_results)
    if total_queries == 0:
        return {"precision_at_k": 0.0, "recall_at_k": 0.0, "mrr": 0.0, "num_queries": 0}

    # Initialize metrics
    sum_precision_at_k = 0.0
    sum_recall_at_k = 0.0
    sum_mrr = 0.0
    num_relevant_queries = 0 # Queries for which we have expected relevant items

    for res in evaluation_results:
        retrieved_hashes = {chunk.get("content_hash") for chunk in res["retrieved_chunks"][:top_k] if chunk.get("content_hash")}
        expected_hashes = set(res["expected_content_hashes"])
        
        if not expected_hashes:
            # Skip queries with no defined relevant documents for precision/recall calculation
            continue
        num_relevant_queries += 1

        # Precision@k
        true_positives = len(retrieved_hashes.intersection(expected_hashes))
        precision_at_k = true_positives / top_k if top_k > 0 else 0.0
        sum_precision_at_k += precision_at_k

        # Recall@k
        recall_at_k = true_positives / len(expected_hashes) if len(expected_hashes) > 0 else 0.0
        sum_recall_at_k += recall_at_k

        # MRR (Mean Reciprocal Rank)
        rr = 0.0
        for i, chunk in enumerate(res["retrieved_chunks"][:top_k]):
            if chunk.get("content_hash") in expected_hashes:
                rr = 1.0 / (i + 1)
                break
        sum_mrr += rr

    avg_precision_at_k = sum_precision_at_k / num_relevant_queries if num_relevant_queries > 0 else 0.0
    avg_recall_at_k = sum_recall_at_k / num_relevant_queries if num_relevant_queries > 0 else 0.0
    avg_mrr = sum_mrr / num_relevant_queries if num_relevant_queries > 0 else 0.0

    return {
        "precision_at_k": avg_precision_at_k,
        "recall_at_k": avg_recall_at_k,
        "mrr": avg_mrr,
        "num_queries_with_expected": num_relevant_queries,
        "total_queries_evaluated": total_queries
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RAG Retrieval Accuracy Validator")
    parser.add_argument("--test-dataset", type=str, required=True,
                        help="Path to the JSON file containing validation queries and expected results.")
    parser.add_argument("--top-k", type=int, default=5,
                        help="Number of top results to consider for precision and recall calculation.")
    
    args = parser.parse_args()

    # T008 [US2]: Load validation dataset
    dataset = load_validation_dataset(args.test_dataset)
    if not dataset:
        logging.error("No dataset loaded. Exiting validation.")
        # Assuming sys is imported elsewhere or should be imported
        # import sys
        # sys.exit(1)

    # T009 [US2]: Execute retrievals for dataset
    evaluation_results = evaluate_retrieval(dataset, top_k=args.top_k)

    # T010 [US2]: Calculate accuracy metrics
    metrics = calculate_accuracy_metrics(evaluation_results, top_k=args.top_k)

    # T011 [US2]: Report accuracy metrics
    print("\n--- Retrieval Accuracy Metrics ---")
    print(f"Top-K for metrics: {args.top_k}")
    print(f"Total queries evaluated: {metrics['total_queries_evaluated']}")
    print(f"Queries with expected relevant items: {metrics['num_queries_with_expected']}")
    print(f"Average Precision@{args.top_k}: {metrics['precision_at_k']:.4f}")
    print(f"Average Recall@{args.top_k}: {metrics['recall_at_k']:.4f}")
    print(f"Mean Reciprocal Rank (MRR): {metrics['mrr']:.4f}")
    print("--------------------------------")
