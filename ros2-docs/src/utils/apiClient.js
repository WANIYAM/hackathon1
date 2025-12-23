const BASE_URL = 'http://127.0.0.1:8000'; // FastAPI backend URL

export const postQuery = async (query, context = null) => {
  try {
    const response = await fetch(`${BASE_URL}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query, context }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error posting query:", error);
    throw error;
  }
};
