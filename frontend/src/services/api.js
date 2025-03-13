// services/api.js
const API_BASE_URL = "http://localhost:8000";

export const fetchLLMResponses = async (
  query,
  selectedLLMs,
  headless = false
) => {
  try {
    const response = await fetch(`${API_BASE_URL}/aggregate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query,
        llms: selectedLLMs,
        headless,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to fetch LLM responses");
    }

    return await response.json();
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
};
