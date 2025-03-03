from typing import Dict, Any
import json
import os
from app.summary_agent_prompt_template import generate_chart_prompt_template, parse_llm_response, generate_chart_prompt_from_json
from app.base_eda import process_file
from app.prompt_template_orchestrator import create_base_template

def process_data_and_generate_eda(file_path: str, output_json: str = None) -> Dict[str, Any]:
    """
    Process input data file and generate EDA results
    """
    return process_file(file_path, output_json)

def generate_dashboard_prompt(file_path: str, user_prompt: str, use_existing_eda: bool = False, eda_json_path: str = None) -> str:
    """
    Generate a prompt for dashboard configuration based on data analysis and user requirements
    """
    if use_existing_eda and eda_json_path:
        return generate_chart_prompt_from_json(eda_json_path, user_prompt)
    else:
        return generate_chart_prompt_template(file_path, user_prompt)

def create_orchestrator_prompt(eda_results: Dict[str, Any]) -> str:
    """
    Create a prompt for the orchestrator agent to guide user interaction
    """
    return create_base_template().format(
        data_quality_summary=eda_results.get('data_quality', {}),
        column_type_summary=eda_results.get('column_types', {}),
        data_insights=eda_results.get('basic_distribution_summary', {}),
        filter_suggestions=eda_results.get('suggested_filters', [])
    )

def process_llm_response(llm_response: str) -> Dict[str, Any]:
    """
    Process and validate LLM response for dashboard configuration
    """
    return parse_llm_response(llm_response)

def main():
    """
    Main entrypoint for the dashboard configuration system
    """
    # Example usage
    sample_data_path = "sample_data.csv"
    
    # Create a sample data file if it doesn't exist (for testing)
    if not os.path.exists(sample_data_path):
        with open(sample_data_path, 'w') as f:
            f.write("order_id,customer_id,order_date,product_category,price,quantity,total_amount,status,payment_method\n")
            f.write("1,101,2023-01-01,Electronics,199.99,1,199.99,delivered,credit_card\n")
            f.write("2,102,2023-01-02,Clothing,49.99,2,99.98,delivered,paypal\n")
    
    # Step 1: Process data and generate EDA
    eda_results = process_data_and_generate_eda(sample_data_path, "eda_output.json")
    
    # Step 2: Create orchestrator prompt
    orchestrator_prompt = create_orchestrator_prompt(eda_results)
    print("\nOrchestrator Prompt:")
    print("-" * 80)
    print(orchestrator_prompt)
    
    # Step 3: Example user prompt (in a real application, this would come from user input)
    user_prompt = """
    I need a dashboard to track our e-commerce sales performance. I want to see:
    1. Sales trends over time
    2. Performance by product category
    3. Payment method distribution
    """
    
    # Step 4: Generate dashboard configuration prompt
    dashboard_prompt = generate_dashboard_prompt(sample_data_path, user_prompt)
    print("\nDashboard Configuration Prompt:")
    print("-" * 80)
    print(dashboard_prompt)
    
    # Step 5: Example LLM response processing (in a real application, this would come from an LLM)
    example_llm_response = """
    {
        "chart1": {
            "chart_type": "Line",
            "description": "Sales trends over time",
            "echart_data_format": "list of objects [{date: <order_date>, value: <total_amount>}]"
        }
    }
    """
    chart_config = process_llm_response(example_llm_response)
    print("\nProcessed Chart Configuration:")
    print("-" * 80)
    print(json.dumps(chart_config, indent=2))

if __name__ == "__main__":
    main()
