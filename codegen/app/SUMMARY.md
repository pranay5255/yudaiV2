# Summary Agent Implementation

## Overview

We've created a Summary Agent that generates dashboard configurations based on data analysis and user requirements. The agent:

1. Analyzes a dataset using the `base_eda.py` module
2. Takes a user's prompt describing their dashboard requirements
3. Generates a prompt template for an LLM to create dashboard chart configurations
4. Parses the LLM's response into a structured JSON format

## Files Created

1. `summary_agent_prompt_template.py`: The main module that generates the prompt template and parses the LLM response
2. `test_summary_agent.py`: A test script that demonstrates how to use the summary agent
3. `README.md`: Documentation on how to use the summary agent

## Key Features

- **Data Analysis Integration**: Seamlessly integrates with the existing `base_eda.py` module to analyze datasets
- **Fallback Mechanisms**: Handles cases where dependencies like pandas and numpy are not available
- **Flexible Input**: Can process either raw data files or pre-computed EDA results in JSON format
- **Robust Response Parsing**: Includes multiple strategies for extracting JSON from LLM responses
- **Comprehensive Documentation**: Includes examples and explanations for all functions

## Usage Example

```python
from codegen.app.summary_agent_prompt_template import generate_chart_prompt_template, parse_llm_response

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