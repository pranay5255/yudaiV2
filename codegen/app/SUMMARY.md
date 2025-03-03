# Summary Agent Implementation

## Overview

The repository implements an intelligent dashboard configuration system with multiple agents working together. The system:

1. Analyzes datasets using the `base_eda.py` module for comprehensive data exploration
2. Uses an Orchestrator Agent to understand user requirements through guided interaction
3. Generates dashboard configurations through a Summary Agent
4. Produces structured JSON output for chart configurations

## Core Components

1. **Base EDA Module** (`base_eda.py`):
   - Performs data quality assessment
   - Infers column types and relationships
   - Detects outliers and patterns
   - Generates distribution summaries
   - Suggests relevant filters

2. **Orchestrator Agent** (`prompt_template_orchestrator.py`):
   - Guides user interaction through structured questions
   - Focuses on understanding business goals
   - Validates assumptions with users
   - Ensures non-technical, friendly communication
   - Uses first-principles thinking for requirement gathering

3. **Summary Agent** (`summary_agent_prompt_template.py`):
   - Generates LLM prompts for dashboard configuration
   - Parses LLM responses into structured JSON
   - Handles multiple response parsing strategies
   - Provides example chart configurations
   - Supports both raw data and pre-computed EDA results

4. **Main Pipeline** (`main.py`):
   - Orchestrates the entire workflow
   - Processes data and generates EDA
   - Creates orchestrator prompts
   - Generates dashboard configurations
   - Handles LLM response processing

## Key Features

- **Comprehensive Data Analysis**: Seamlessly integrates with `base_eda.py` for thorough data exploration
- **Intelligent Interaction**: Uses an Orchestrator Agent for user-friendly requirement gathering
- **Flexible Input Processing**: Handles both raw data files and pre-computed EDA results
- **Robust Response Handling**: Multiple strategies for parsing LLM responses
- **Example-Driven Development**: Includes sample configurations and usage examples
- **Modular Architecture**: Clear separation of concerns between components

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
  }
}
``` 

config = {
    'methods': ['GET', 'POST'],
    'file_path': "'data/sample.csv'",
    'content_type': "'text/csv'",
    'method_imports': 'import { headers } from "next/headers";',
    'method_params': 'request: Request'
}

api_code = generate_api_route(config)