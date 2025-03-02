# LLM Response Aggregator

A tool to automatically query multiple LLM providers (ChatGPT, Mistral, Grok), evaluate their responses, and determine the best answer.

## Overview

The LLM Response Aggregator is a Python application that helps you:

- Send the same query to multiple LLMs simultaneously
- Extract their responses using browser automation
- Compare model outputs side by side
- Evaluate and rank responses based on relevance, content similarity, and length
- Return the best response and save all results for comparison

## Features

- **Multi-LLM Support**: Currently supports Mistral, and Grok
- **Browser Automation**: Handles web interactions automatically
- **Response Evaluation**: Ranks answers based on query relevance, cross-checking with other LLMs, and optimal length
- **Headless Mode**: Can run without visible browsers for background operation
- **Results Storage**: Saves all responses and their scores in JSON format

## Installation

### Prerequisites

- Python 3.10+
- Chrome browser installed
- ChromeDriver compatible with your Chrome version

### Setup

1. Clone this repository:

```bash
git clone https://github.com/moatasem75291/LLMs-response-aggregator.git
cd llm-response-aggregator
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

3. Install dependencies:

```python
pip install -r requirements.txt
```

### Usage

#### Basic Usage

Run the tool with a query:

```python
python main.py --query "Explain quantum computing"
```

If you don't provide a query, you'll be prompted to enter one.

#### Command Line Options

```python
python main.py [options]

Options:
  --query TEXT        Query to send to LLMs
  --llms LIST         LLMs to query (default: chatgpt mistral grok)
  --no-headless       Run browsers in visible mode (not headless)
```

#### Examples

Query specific LLMs:

```python
python main.py --llms chatgpt grok --query "How does blockchain work?"
```

Show browser interactions (for debugging):

```python
python main.py --query "Explain machine learning" --no-headless
```

### Project Structure:

```css
llm_aggregator/
├── __init__.py
├── main.py                   # Entry point
├── config/
│   ├── __init__.py
│   └── llm_configs.py        # Configuration for each LLM
├── core/
│   ├── __init__.py
│   ├── aggregator.py         # Main aggregator class
│   ├── browser.py            # Browser automation
│   └── evaluator.py          # Response evaluation logic
├── utils/
│   ├── __init__.py
│   └── storage.py            # Result storage utilities
└── requirements.txt          # Dependencies
```

### Adding New LLMs

To add support for a new LLM:

1. Add configuration in [config/llm_configs.py](config/llm_configs.py):

```python
LLM_CONFIGS = {
    # Existing LLMs...
    "new_llm": {
        "url": "https://new-llm-website.com/",
        "input_selector": "css.selector.for.input",
        "response_selector": "css.selector.for.response",
        "wait_time": 30,  # seconds
    },
}
```

2. If the LLM requires special handling, modify [core/browser.py](core/browser.py) to accommodate its interface.

### How It Works

1. **Query Input**: The application takes a user query as input.
2. **Browser Automation**: It launches Chrome instances (headless by default) to interact with each LLM's web interface.
3. **Response Collection**: It submits the query to each LLM and waits for responses.
4. **Evaluation**: Responses are evaluated using:
   - Relevance to the original query (50% weight)
   - Cross-check similarity with other responses (30% weight)
   - Optimal length scoring (20% weight)
5. **Result Presentation**: The highest-scoring response is displayed and all responses are saved to a JSON file.

### Troubleshooting

- **Chrome Issues**: Make sure your Chrome browser and ChromeDriver versions are compatible.
- **Selector Problems**: If an LLM changes its web interface, update the CSS selectors in the configuration.
- **Timeout Errors**: Increase the `wait_time` in the LLM's configuration if responses are taking longer.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
