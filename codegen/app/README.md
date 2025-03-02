# Dashboard Configuration Agent

This module provides tools to generate dashboard configurations based on data analysis and user requirements.

## Overview

The Summary Agent is designed to:

1. Analyze a dataset using the `base_eda.py` module
2. Take a user's prompt describing their dashboard requirements
3. Generate a prompt template for an LLM to create dashboard chart configurations
4. Parse the LLM's response into a structured JSON format

## Files

- `base_eda.py`: Performs exploratory data analysis on a dataset
- `summary_agent_prompt_template.py`: Generates a prompt template for the LLM
- `test_summary_agent.py`: Demonstrates how to use the summary agent

## Usage

### Basic Usage

```python
from summary_agent_prompt_template import generate_chart_prompt_template, parse_llm_response

# Path to your data file
file_path = "your_data.csv"

# User's requirements
user_prompt = """
I need a dashboard to track our e-commerce sales performance. I want to see:
1. Sales trends over time
2. Performance by product category
3. Payment method distribution
"""

# Generate the prompt template
prompt = generate_chart_prompt_template(file_path, user_prompt)

# Send the prompt to an LLM (not included in this module)
llm_response = your_llm_function(prompt)

# Parse the LLM's response
chart_config = parse_llm_response(llm_response)

# Use the chart configuration to build your dashboard
print(chart_config)
```

### Using Pre-existing EDA Results

If you've already run the EDA and saved the results to a JSON file:

```python
from summary_agent_prompt_template import generate_chart_prompt_from_json, parse_llm_response

# Path to your EDA results JSON file
eda_json_path = "eda_results.json"

# User's requirements
user_prompt = "I need a dashboard to track sales performance..."

# Generate the prompt template
prompt = generate_chart_prompt_from_json(eda_json_path, user_prompt)

# Send the prompt to an LLM (not included in this module)
llm_response = your_llm_function(prompt)

# Parse the LLM's response
chart_config = parse_llm_response(llm_response)
```

## Output Format

The output is a JSON object with chart configurations:

```json
{
  "chart1": {
    "chart_type": "Line",
    "description": "A line chart showing sales trends over time",
    "echart_data_format": "list of objects [{date: <order_date>, value: <total_amount>}]",
    "chart_Xaxis": "order_date",
    "chart_Yaxis": "total_amount",
    "example_function": "function generateLineChartOptions(data, xKey, yKey, title) {...}",
    "prompt_used": "Show sales trends over time",
    "extra_options": {
      "smooth": true,
      "areaStyle": true,
      "tooltip": true
    }
  },
  "chart2": {
    "chart_type": "Bar",
    "description": "A bar chart showing sales by product category",
    ...
  },
  ...
}
```

## Running the Test

To run the test script:

```bash
python test_summary_agent.py
```

This will demonstrate the full workflow using a sample dataset and user prompt. 