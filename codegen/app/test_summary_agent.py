import json
import os
from summary_agent_prompt_template import generate_chart_prompt_template, parse_llm_response

def main():
    """
    Test the summary agent prompt template with a sample user prompt and EDA output
    """
    # Sample user prompt
    user_prompt = """
    I need a dashboard to track our e-commerce sales performance. I want to see:
    1. Sales trends over time
    2. Performance by product category
    3. Payment method distribution
    4. Order status breakdown
    5. Shipping type analysis
    
    I'd like to be able to filter by date range and product category.
    """
    
    # Create a sample data file for testing
    sample_data_path = "sample_data.csv"
    
    # Create a simple CSV file if it doesn't exist
    if not os.path.exists(sample_data_path):
        with open(sample_data_path, 'w') as f:
            f.write("order_id,customer_id,order_date,product_category,price,quantity,total_amount,status,payment_method\n")
            f.write("1,101,2023-01-01,Electronics,199.99,1,199.99,delivered,credit_card\n")
            f.write("2,102,2023-01-02,Clothing,49.99,2,99.98,delivered,paypal\n")
            f.write("3,103,2023-01-03,Books,19.99,3,59.97,processing,debit_card\n")
            f.write("4,104,2023-01-04,Electronics,299.99,1,299.99,in_transit,credit_card\n")
            f.write("5,105,2023-01-05,Furniture,499.99,1,499.99,delivered,bank_transfer\n")
    
    # Generate the prompt template
    prompt = generate_chart_prompt_template(sample_data_path, user_prompt)
    
    # Print the generated prompt
    print("Generated Prompt Template:")
    print("-" * 80)
    print(prompt)
    print("-" * 80)
    
    # In a real application, you would send this prompt to an LLM
    # and then parse the response
    
    # For demonstration purposes, let's use a mock LLM response
    mock_llm_response = """
    ```json
    {
        "chart1": {
            "chart_type": "Line",
            "description": "A line chart showing sales trends over time",
            "echart_data_format": "list of objects [{date: <order_date>, value: <total_amount>}]",
            "chart_Xaxis": "order_date",
            "chart_Yaxis": "total_amount",
            "example_function": "function generateLineChartOptions(data, xKey, yKey, title) {\\n    return { title: { text: title }, xAxis: { type: 'time', data: data.map(d => d[xKey]) }, yAxis: { type: 'value' }, series: [{ type: 'line', data: data.map(d => d[yKey]), smooth: true }] };\\n}",
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
            "echart_data_format": "list of objects [{category: <product_category>, value: <total_amount>}]",
            "chart_Xaxis": "product_category",
            "chart_Yaxis": "total_amount",
            "example_function": "function generateBarChartOptions(data, xKey, yKey, title) {\\n    return { title: { text: title }, xAxis: { type: 'category', data: data.map(d => d[xKey]) }, yAxis: { type: 'value' }, series: [{ type: 'bar', data: data.map(d => d[yKey]) }] };\\n}",
            "prompt_used": "Show sales by product category",
            "extra_options": {
                "color": "auto",
                "legend": true
            }
        },
        "chart3": {
            "chart_type": "Pie",
            "description": "A pie chart showing distribution of payment methods",
            "echart_data_format": "list of objects [{name: <payment_method>, value: <count>}]",
            "chart_Xaxis": "payment_method",
            "chart_Yaxis": "count",
            "example_function": "function generatePieChartOptions(data, valueKey, nameKey, title) {\\n    return { title: { text: title }, tooltip: { trigger: 'item' }, series: [{ type: 'pie', data: data.map(d => ({ value: d[valueKey], name: d[nameKey] })) }] };\\n}",
            "prompt_used": "Show payment method distribution",
            "extra_options": {
                "tooltip": true,
                "legend": true
            }
        },
        "chart4": {
            "chart_type": "Pie",
            "description": "A pie chart showing order status breakdown",
            "echart_data_format": "list of objects [{name: <status>, value: <count>}]",
            "chart_Xaxis": "status",
            "chart_Yaxis": "count",
            "example_function": "function generatePieChartOptions(data, valueKey, nameKey, title) {\\n    return { title: { text: title }, tooltip: { trigger: 'item' }, series: [{ type: 'pie', data: data.map(d => ({ value: d[valueKey], name: d[nameKey] })) }] };\\n}",
            "prompt_used": "Show order status breakdown",
            "extra_options": {
                "tooltip": true,
                "legend": true
            }
        },
        "chart5": {
            "chart_type": "Bar",
            "description": "A bar chart showing shipping type analysis",
            "echart_data_format": "list of objects [{type: <shipping_type>, value: <count>}]",
            "chart_Xaxis": "shipping_type",
            "chart_Yaxis": "count",
            "example_function": "function generateBarChartOptions(data, xKey, yKey, title) {\\n    return { title: { text: title }, xAxis: { type: 'category', data: data.map(d => d[xKey]) }, yAxis: { type: 'value' }, series: [{ type: 'bar', data: data.map(d => d[yKey]) }] };\\n}",
            "prompt_used": "Show shipping type analysis",
            "extra_options": {
                "color": "auto",
                "legend": true
            }
        }
    }
    ```
    """
    
    # Parse the LLM response
    chart_config = parse_llm_response(mock_llm_response)
    
    # Print the parsed chart configuration
    print("\nParsed Chart Configuration:")
    print("-" * 80)
    print(json.dumps(chart_config, indent=2))
    print("-" * 80)

if __name__ == "__main__":
    main() 