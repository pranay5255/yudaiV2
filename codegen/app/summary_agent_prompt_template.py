from typing import Dict, Any, List
import json
import os
from .context_manager import ContextManager

def create_base_template() -> str:
    """Returns the enhanced summary agent template"""
    return '''
    You are a Dashboard Configuration Agent responsible for generating comprehensive JSON configurations for interactive dashboards based on data analysis, historical context, and user requirements.

    Your task is to generate a detailed JSON configuration that defines multiple chart components for an interactive dashboard. Each chart definition must include:

    Required Properties:
    - chart_id: Unique identifier for the chart
    - chart_type: The visualization type (e.g., "Pie", "Bar", "Line", "Scatter", "Radar", "Table", "Heatmap")
    - title: Clear, descriptive title for the chart
    - description: Detailed explanation of what the chart displays and its insights
    - data_requirements: {
        - required_columns: List of data columns needed
        - aggregations: Required data aggregations
        - filters: Suggested data filters
        - transformations: Any data transformations needed
      }
    - visual_config: {
        - x_axis: Configuration for x-axis (name, type, format)
        - y_axis: Configuration for y-axis (name, type, format)
        - series: Series configuration including colors, styles
        - tooltip: Tooltip configuration
        - legend: Legend configuration
      }
    - interactions: {
        - drill_down: Drill-down capabilities
        - filters: Interactive filter options
        - highlights: Highlight interactions
      }
    - api_requirements: {
        - endpoint: Required API endpoint pattern
        - parameters: Expected query parameters
        - response_format: Expected response format
      }

    Context Information:
    
    Dataset Analysis:
    {data_quality_summary}

    Column Information:
    {column_type_summary}

    Key Insights:
    {data_insights}

    Historical Context:
    {historical_context}

    User Requirements:
    {user_prompt}

    Suggested Interactions:
    {filter_suggestions}

    Generate a complete dashboard configuration with 3-5 complementary charts that:
    1. Address the user's specific requirements
    2. Highlight key insights from the data
    3. Provide meaningful interactive capabilities
    4. Enable data exploration through filters and drill-downs
    5. Follow visualization best practices

    Respond with a valid JSON configuration that can be directly used by the Dashboard and API components.
    '''

def format_data_quality_summary(data_quality: Dict[str, Any]) -> str:
    """Format the data quality information into a readable summary"""
    return f"""- Dataset contains {data_quality['row_count']} rows and {data_quality['column_count']} columns
- Overall data completeness: {100 - data_quality['missing_value_percentage']:.1f}%
- Number of duplicate rows: {data_quality['duplicate_row_count']}"""

def format_column_type_summary(column_types: Dict[str, list]) -> str:
    """Format the column type information into a readable summary"""
    summary = []
    if column_types.get('datetime'):
        summary.append(f"- Time-based columns: {', '.join(column_types['datetime'])}")
    if column_types.get('numeric'):
        summary.append(f"- Numeric columns: {', '.join(column_types['numeric'])}")
    if column_types.get('categorical_low_cardinality'):
        summary.append(f"- Category columns (few unique values): {', '.join(column_types['categorical_low_cardinality'])}")
    if column_types.get('categorical_high_cardinality'):
        summary.append(f"- Text columns (many unique values): {', '.join(column_types['categorical_high_cardinality'])}")
    return "\n".join(summary)

def format_data_insights(distribution_summary: Dict[str, Dict], outlier_report: Dict) -> str:
    """Format the distribution and outlier information into readable insights"""
    insights = []
    for col, stats in distribution_summary.items():
        if 'mean' in stats:  # Numeric column
            insights.append(f"- {col}: Average {stats['mean']:.2f}, ranges from {stats['min']:.2f} to {stats['max']:.2f}")
        elif 'top_values' in stats:  # Categorical column
            top_vals = list(stats['top_values'].items())[:3]
            insights.append(f"- {col}: Most common values are {', '.join(f'{val} ({count})' for val, count in top_vals)}")
    
    for col, stats in outlier_report.items():
        if stats['outlier_count'] > 0:
            insights.append(f"- {col}: Contains {stats['outlier_count']} outliers")
    
    return "\n".join(insights)

def format_filter_suggestions(suggested_filters: list, date_frequencies: Dict[str, str]) -> str:
    """Format the filter suggestions into a readable summary"""
    suggestions = suggested_filters.copy()
    for col, freq in date_frequencies.items():
        if freq != "Irregular":
            suggestions.append(f"Time-based analysis possible on '{col}' ({freq} frequency)")
    return "\n".join(f"- {suggestion}" for suggestion in suggestions)

def format_historical_context(context: Dict[str, Any]) -> str:
    """Format historical context from previous analyses and user interactions"""
    history = []
    
    # Add previous user inputs
    if context.get('user_inputs'):
        recent_inputs = context['user_inputs'][-3:]  # Get last 3 inputs
        history.append("Recent User Queries:")
        for input_entry in recent_inputs:
            history.append(f"- {input_entry['input']} ({input_entry['timestamp']})")
    
    # Add relevant previous analyses
    if context.get('analysis_history'):
        recent_analyses = context['analysis_history'][-2:]  # Get last 2 analyses
        history.append("\nPrevious Analysis Insights:")
        for analysis in recent_analyses:
            if 'key_findings' in analysis['analysis']:
                history.append(f"- {analysis['analysis']['key_findings']}")
    
    return "\n".join(history)

def generate_chart_prompt_template(file_path: str, user_prompt: str, context_manager: ContextManager) -> str:
    """Generate a complete prompt template with data analysis results, historical context, and user prompt"""
    from codegen.app.base_eda import process_file
    
    # Get current analysis context
    current_context = process_file(file_path)
    
    # Add current analysis to context manager
    context_manager.add_analysis_result(current_context)
    
    # Get historical context
    full_context = context_manager.get_context()
    historical_context = format_historical_context(full_context)
    
    template = create_base_template()
    return template.format(
        data_quality_summary=format_data_quality_summary(current_context['data_quality']),
        column_type_summary=format_column_type_summary(current_context['column_types']),
        data_insights=format_data_insights(
            current_context['basic_distribution_summary'],
            current_context['outlier_report']
        ),
        filter_suggestions=format_filter_suggestions(
            current_context['suggested_filters'],
            current_context['date_frequencies']
        ),
        historical_context=historical_context,
        user_prompt=user_prompt
    )

def parse_llm_response(response: str) -> Dict:
    """Parse the LLM response to extract the JSON configuration"""
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        import re
        json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        json_match = re.search(r'({[\s\S]*})', response)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        return {}

def example_chart_config() -> Dict:
    """Returns an enhanced example chart configuration"""
    return {
        "dashboard_config": {
            "title": "Sales Performance Dashboard",
            "description": "Interactive dashboard showing sales performance metrics",
            "layout": "responsive",
            "theme": "light",
            "charts": [
                {
                    "chart_id": "sales_trend",
                    "chart_type": "Line",
                    "title": "Sales Trend Over Time",
                    "description": "Shows the trend of sales over time with the ability to filter by product category",
                    "data_requirements": {
                        "required_columns": ["date", "sales_amount", "product_category"],
                        "aggregations": ["sum", "average"],
                        "filters": ["date_range", "product_category"],
                        "transformations": ["daily_to_monthly"]
                    },
                    "visual_config": {
                        "x_axis": {
                            "type": "time",
                            "name": "Date",
                            "format": "YYYY-MM-DD"
                        },
                        "y_axis": {
                            "type": "value",
                            "name": "Sales Amount",
                            "format": "currency"
                        },
                        "series": {
                            "type": "line",
                            "smooth": True,
                            "color": ["#91cc75"]
                        },
                        "tooltip": {
                            "trigger": "axis",
                            "formatter": "{b}: ${c}"
                        },
                        "legend": {
                            "show": True,
                            "position": "top"
                        }
                    },
                    "interactions": {
                        "drill_down": {
                            "enabled": True,
                            "levels": ["year", "quarter", "month", "day"]
                        },
                        "filters": ["category", "date_range"],
                        "highlights": ["click", "hover"]
                    },
                    "api_requirements": {
                        "endpoint": "/api/sales/trend",
                        "parameters": {
                            "start_date": "string",
                            "end_date": "string",
                            "category": "string",
                            "aggregation": "string"
                        },
                        "response_format": {
                            "dates": "array",
                            "values": "array",
                            "categories": "array"
                        }
                    }
                }
                # ... additional chart configurations ...
            ]
        }
    }

if __name__ == "__main__":
    # Example usage
    file_path = "sample_data.csv"
    user_prompt = "Create a sales dashboard with trend analysis, category breakdown, and payment method distribution."
    
    # Initialize context manager
    context_manager = ContextManager("sales_dashboard_context.json")
    
    # Generate prompt template
    prompt = generate_chart_prompt_template(file_path, user_prompt, context_manager)
    print(prompt)
    
    # Example of what the output might look like
    print("\nExample output configuration:")
    print(json.dumps(example_chart_config(), indent=2)) 