import asyncio
import logging
import argparse
from datetime import datetime
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


async def main():
    """Entry point for the LLM Response Aggregator."""
    parser = argparse.ArgumentParser(
        description="Aggregate responses from multiple LLMs"
    )

    parser.add_argument("--query", type=str, help="Query to send to LLMs")
    parser.add_argument(
        "--llms",
        type=str,
        nargs="+",
        default=["chatgpt", "deepseek", "grok"],
        help="LLMs to query (default: all)",
    )
    parser.add_argument(
        "--no-headless",
        action="store_true",
        help="Run browsers in visible mode (not headless)",
    )

    args = parser.parse_args()
    # Get query from command line or user input
    query = args.query
    if not query:
        query = input("Enter your query: ")

    # Process the query
    logger.info(f"Processing query: {query}")
    aggregator = LLMResponseAggregator(
        selected_llms=args.llms, headless=not args.no_headless
    )

    try:
        result = await aggregator.process_query(query)

        # Display the best response
        if "error" in result:
            logger.error(f"Error: {result['error']}")
        else:
            print("\n--- Best Response ---")
            print(f"Source: {result['best_response']['source']}")
            print(f"Score: {result['best_response']['score']:.2f}")
            print(f"Content:\n{result['best_response']['content']}")

            # Log file location
            filename = result.get("filename", "")
            if filename:
                print(f"\nAll responses saved to: {filename}")

        return result
    except Exception as e:
        logger.exception(f"Error in main process: {str(e)}")
        return {"error": str(e)}


if __name__ == "__main__":
    asyncio.run(main())
