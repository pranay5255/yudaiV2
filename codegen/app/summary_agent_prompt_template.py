from typing import Dict, Any, List
import json
import os

def create_base_template() -> str:
    """Returns the base summary agent template"""
    return '''
    You are a Dashboard Configuration Agent whose job is to generate JSON configurations for interactive dashboards based on data analysis and user requirements.

    Your task is to generate a JSON configuration that defines multiple chart components for an interactive dashboard. The configuration must include five chart definitions with the following properties:

    - chart_type: The type of chart (e.g., "Pie", "Bar", "Line", "Scatter", "Radar", "Table", "Heatmap")
    - description: A short explanation of what the chart displays
    - echart_data_format: A string that describes the expected data format
    - chart_Xaxis: The data column used for the X-axis
    - chart_Yaxis: The data column used for the Y-axis
    - example_function: A code snippet (JavaScript function) that demonstrates how to generate the chart options
    - prompt_used: The prompt or user instruction that triggered the creation of the chart
    - extra_options: Additional configuration options (e.g., tooltips, legends, colors, stacking, smooth curves)

    Based on the analysis of the provided data:

    {data_quality_summary}

    The data contains the following key characteristics:
    {column_type_summary}

    Key insights from the data:
    {data_insights}

    Suggested filters and views:
    {filter_suggestions}

    User's requirements:
    {user_prompt}

    Using this information, create five chart configurations that would be most useful for exploring this dataset and meeting the user's needs. Your output must be strictly in JSON format.
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

def generate_chart_prompt_template(file_path: str, user_prompt: str) -> str:
    """Generate a complete prompt template with data analysis results and user prompt"""
    from codegen.app.base_eda import process_file
    context = process_file(file_path)
    
    template = create_base_template()
    return template.format(
        data_quality_summary=format_data_quality_summary(context['data_quality']),
        column_type_summary=format_column_type_summary(context['column_types']),
        data_insights=format_data_insights(
            context['basic_distribution_summary'],
            context['outlier_report']
        ),
        filter_suggestions=format_filter_suggestions(
            context['suggested_filters'],
            context['date_frequencies']
        ),
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
    """Returns an example chart configuration for reference"""
    return {
        "chart1": {
            "chart_type": "Pie",
            "description": "A pie chart showing the proportion of categories in the dataset.",
            "echart_data_format": "list of objects [{name: <category_name>, value: <numeric_value>}]",
            "chart_Xaxis": "category_column",
            "chart_Yaxis": "value_column",
            "example_function": "function generatePieChartOptions(data, valueKey, nameKey, title) {\n    return { title: { text: title }, tooltip: { trigger: 'item' }, series: [{ type: 'pie', data: data.map(d => ({ value: d[valueKey], name: d[nameKey] })) }] };\n}",
            "prompt_used": "Show a breakdown of product sales by category.",
            "extra_options": {
                "tooltip": True,
                "legend": True
            }
        },
        "chart2": {
            "chart_type": "Bar",
            "description": "A bar chart showing the sales of different products over time.",
            "echart_data_format": "list of objects [{x: <x_axis_value>, y: <y_axis_value>}]",
            "chart_Xaxis": "product_column",
            "chart_Yaxis": "sales_column",
            "example_function": "function generateBarChartOptions(data, xKey, yKey, title) {\n    return { title: { text: title }, xAxis: { type: 'category', data: data.map(d => d[xKey]) }, yAxis: { type: 'value' }, series: [{ type: 'bar', data: data.map(d => d[yKey]) }] };\n}",
            "prompt_used": "Show product-wise sales over the past year.",
            "extra_options": {
                "stacked": False,
                "color": "auto"
            }
        }
    }

if __name__ == "__main__":
    # Example usage
    file_path = "sample_data.csv"
    user_prompt = "I need a dashboard to track sales performance by product category over time, with the ability to filter by payment method and shipping type."
    
    # Generate prompt template
    prompt = generate_chart_prompt_template(file_path, user_prompt)
    print(prompt)
    
    # Example of using a pre-existing EDA JSON
    # prompt = generate_chart_prompt_from_json("codegen/app/example_eda_output.json", user_prompt)
    # print(prompt)
    
    # Example of what the output might look like
    print("\nExample output configuration:")
    print(json.dumps(example_chart_config(), indent=2)) 