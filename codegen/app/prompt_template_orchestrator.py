from typing import Dict, Any, List
from app.models import DatasetProfile
from datetime import datetime

def create_base_template() -> str:
    """Returns the base orchestrator template with the 7 fundamental questions"""
    return '''
    You are a friendly Orchestrator Agent whose job is to understand a user's needs so you can help create the perfect dashboard for them. 

    Use this set of 7 critical questions as your foundation:
    1. What is the main goal of the dashboard? (Understand their objective)
    2. What type of data have they uploaded? (Understand the data structure — list, timeline, reviews, etc.)
    3. What kind of analysis do they want? (See what happened, understand why, predict future, or suggest actions)
    4. What numbers or facts matter most? (Key metrics or facts they want to track)
    5. How do they want to see the information? (Charts, tables, timelines — visual preferences)
    6. Do they want filters to focus on certain products, regions, or time periods?
    7. Who will use this dashboard? (Just them, their team, their manager — audience matters)

    You have 2 turns to engage with the user:
    Turn 1: Share a data quality insight and ask questions about goals and data understanding (Questions 1-3)
    Turn 2: Share an analysis possibility insight and ask about visualization and usage preferences (Questions 4-7)

    Be friendly, clear, and always tie your insights to relevant questions.
    '''

def _create_first_turn_insight(profile: DatasetProfile) -> str:
    """Generate first turn insight focusing on data quality and structure"""
    insights = [
        f"I see your dataset has {profile.table.n_duplicates} duplicate rows ({profile.table.p_duplicates:.1%}), what is the main goal of your analysis - should we focus on data cleaning first?",
        f"Your dataset contains {len(profile.variables)} columns with {profile.table.p_cells_missing:.1%} missing values overall, what type of insights are you hoping to discover?",
        f"I notice you have {profile.table.types.get('DateTime', 0)} time-based columns spanning from {profile.analysis.date_start} to {profile.analysis.date_end}, what temporal patterns interest you most?"
    ]
    
    # Choose most relevant insight based on data characteristics
    if profile.table.p_duplicates > 0.1:
        return insights[0]
    elif profile.table.p_cells_missing > 0.1:
        return insights[1]
    else:
        return insights[2]

def _create_second_turn_insight(profile: DatasetProfile) -> str:
    """Generate second turn insight focusing on analysis possibilities"""
    insights = [
        f"The data shows interesting correlations between numeric variables, how would you prefer to visualize these relationships - through charts, tables, or both?",
        f"There are {len(profile.variables)} different metrics available, which specific numbers or trends matter most for your stakeholders?",
        f"Your categorical columns like {list(profile.variables.keys())[:2]} could be useful filters, what specific segments of the data do you want to focus on?"
    ]
    
    # Choose based on data characteristics
    has_numeric = any(v.type == "Numeric" for v in profile.variables.values())
    has_categorical = any(v.type == "Categorical" for v in profile.variables.values())
    
    if has_numeric:
        return insights[0]
    elif has_categorical:
        return insights[2]
    else:
        return insights[1]

def generate_prompt_template(profile: DatasetProfile, turn: int = 1) -> str:
    """Generate a complete prompt template with dataset insights"""
    base_template = create_base_template()
    
    if turn == 1:
        insight = _create_first_turn_insight(profile)
    else:
        insight = _create_second_turn_insight(profile)
    
    return f"{base_template}\n\nBased on the current data:\n{insight}"

if __name__ == "__main__":
    # Example usage
    import sys
    import json
    
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            profile_data = json.load(f)
            profile = DatasetProfile(**profile_data)
            
            print("\nTurn 1:")
            print(generate_prompt_template(profile, 1))
            print("\nTurn 2:")
            print(generate_prompt_template(profile, 2))
    else:
        print("Please provide a path to a profile JSON file") 