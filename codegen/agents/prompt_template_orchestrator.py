from typing import Dict, Any
from app.models import DatasetProfile
from datetime import datetime
from .dataset_profiler_agent import DatasetProfilerAgent
from .insight_gen_agent import InsightGenAgent

def create_base_template() -> str:
    """Returns the base orchestrator template with the 7 fundamental questions"""
    return '''
    You are a friendly Orchestrator Agent whose job is to understand a user's needs so you can help create the perfect dashboard for them. 

    Use these 7 critical questions as your foundation:
    1. What is the main goal of the dashboard? (Understand their objective)
    2. What type of data have they uploaded? (Understand the data structure — list, timeline, reviews, etc.)
    3. What kind of analysis do they want? (See what happened, understand why, predict future, or suggest actions)
    4. What numbers or facts matter most? (Key metrics or facts they want to track)
    5. How do they want to see the information? (Charts, tables, timelines — visual preferences)
    6. Do they want filters to focus on certain products, regions, or time periods?
    7. Who will use this dashboard? (Just them, their team, their manager — audience matters)

    Based on the data profile, provide one insight and ask one relevant question from the above list.
    '''
#   Add Agent open ai api to simualate conversation for agent.  
# Add base_eda.py to add insight and question to prompt template.
# Call LLM api with prompt template to generate insight and question.
def generate_prompt_template(profile: DatasetProfile) -> str:
    """Generate a complete prompt template with dataset insight and a question"""
    # Initialize agents
    profiler_agent = DatasetProfilerAgent()
    insight_agent = InsightGenAgent()
    
    # Generate profile summary
    profile_summary = profiler_agent.generate_profile_summary(profile)
    
    # Generate insight and question
    insight, question = insight_agent.generate_insight_and_question(profile_summary)
    
    return f"""
    You are a friendly Orchestrator Agent whose job is to understand a user's needs so you can help create the perfect dashboard for them. 

    Based on the current data:
    {insight}

    {question}
    """

if __name__ == "__main__":
    # Example usage
    import sys
    import json
    
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            profile_data = json.load(f)
            profile = DatasetProfile(**profile_data)
            print(generate_prompt_template(profile))
    else:
        print("Please provide a path to a profile JSON file") 