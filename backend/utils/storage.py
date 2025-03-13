import json
import os
import logging
from datetime import datetime


logger = logging.getLogger(__name__)


def store_result(result, output_dir="results"):
    """
    Store the result to a JSON file.

    Args:
        result: Dictionary containing the result.
        output_dir: Directory to store the results.

    Returns:
        Path to the stored file.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_dir, f"llm_responses_{timestamp}.json")

    try:
        with open(filename, "w") as f:
            json.dump(result, f, indent=4, default=str)
        logger.info(f"Result stored at: {filename}")
        return filename
    except Exception as e:
        logger.error(f"Error storing result: {str(e)}")
        return None
