import logging
from datetime import datetime
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from core.aggregator import LLMResponseAggregator

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"aggregator_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


# Define request model
class QueryRequest(BaseModel):
    query: str
    llms: list[str] = ["chatgpt", "deepseek", "grok", "mistral"]
    headless: bool = True


@app.post("/aggregate")
async def aggregate_responses(request: QueryRequest):
    """Endpoint to aggregate responses from multiple LLMs."""
    logger.info(f"Processing query: {request.query}")
    aggregator = LLMResponseAggregator(
        selected_llms=request.llms, headless=request.headless
    )

    try:
        result = await aggregator.process_query(request.query)
        if "error" in result:
            logger.error(f"Error: {result['error']}")
            raise HTTPException(status_code=500, detail=result["error"])

        return HTTPException(status_code=200, detail=result)

    except Exception as e:
        logger.exception(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# To run the FastAPI app, use: `uvicorn main:app --host 0.0.0.0 --port 8000`
