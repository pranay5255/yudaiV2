from typing import Dict, Any
import json
from app.models import DatasetProfile
from .context_manager import Context

def create_base_template() -> str:
    """Returns the enhanced summary agent template for ECharts configuration"""
    return '''
    You are a Dashboard Configuration Agent responsible for generating ECharts configurations for interactive dashboards based on data analysis and user requirements.

    Your task is to generate a JSON configuration that defines 4 complementary chart components using ECharts.

    Dataset Profile:
    {dataset_profile}

    User Requirements:
    {user_requirements}

    Generate exactly 4 complementary charts that address the user's requirements and highlight key insights from the dataset.
    '''

# User requirements is the output from the prompt template orchestrator.
# Dataset profile is the output from the base_eda.py
# summary agent will use the user requirements and dataset profile to generate 4 compementary chartconfig.json
# Split this fucntionality into 2 parts:
# 1. 1st agent only thinks and reasons about which charts that should be in the dashboard based on the user requirements and dataset profile.
# 2. 2nd agent will generate the JSON configuration for the charts.

def format_dataset_profile(profile: DatasetProfile) -> str:
    """Format the dataset profile into a readable summary"""
    if not profile:
        return "No dataset profile available"
        
    if isinstance(profile, dict):
        profile = DatasetProfile(**profile)
        
    summary = [
        f"Dataset: {profile.analysis.title}",
        f"Rows: {profile.table.n:,}",
        f"Columns: {profile.table.n_var}",
        f"Date Range: {profile.analysis.date_start} to {profile.analysis.date_end}",
        "\nKey Variables:"
    ]
    
    for var_name, var_info in profile.variables.items():
        summary.append(f"- {var_name} ({var_info.type})")
    
    return "\n".join(summary)

def generate_chart_prompt_template(profile: DatasetProfile, user_requirements: str) -> str:
    """Generate a complete prompt template with dataset profile"""
    template = create_base_template()
    
    if not profile:
        raise ValueError("Profile is required to generate the prompt template")
    
    if isinstance(profile, dict):
        profile = DatasetProfile(**profile)
    
    return template.format(
        dataset_profile=format_dataset_profile(profile),
        user_requirements=user_requirements
    )

def parse_llm_response(response: str) -> Dict:
    """Parse the LLM response to extract the JSON configuration"""
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        import re
        json_match = re.search(r'```(?:json)?\n(.*?)\n```', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        return {}

if __name__ == "__main__":
    # Example usage
    from context_manager import ContextManager
    
    context_manager = ContextManager()
    profile = context_manager.get_dataset_profile()
    
    if profile:
        try:
            prompt = generate_chart_prompt_template(profile, "Show me sales trends over time")
            print(prompt)
        except Exception as e:
            print(f"Error generating prompt template: {e}")
    else:
        print("No dataset profile available. Please upload a dataset first.") 