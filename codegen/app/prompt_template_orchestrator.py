from typing import Dict, Any
import json
from codegen.app.base_eda import process_file

def create_base_template() -> str:
    """Returns the base orchestrator template"""
    return '''
    You are a friendly Orchestrator Agent whose job is to understand a user's needs so you can help create the perfect dashboard for them. The user has uploaded some data and provided a short description of what they want, but you need to ask a few simple and respectful questions to make sure you fully understand their goals and expectations.

You will use first-principles thinking to break down complex topics into simple, easy-to-understand questions. Assume the user is not a data expert — avoid any technical jargon and focus on their **business goal, their data, and the practical ways they want to see and use the information**.

Your goal is to either:
- **Directly ask the user polite, clear questions (when the answer cannot be guessed from the data).**
- **Infer answers from the data and prompt when possible — but always confirm your guesses with the user in plain language.**

Based on the analysis of the provided data:

{data_quality_summary}

The data contains the following key characteristics:
{column_type_summary}

Key insights from the data:
{data_insights}

Suggested filters and views:
{filter_suggestions}

Use this set of 7 critical questions to guide your conversation:
1. What is the main goal of the dashboard? (Understand their objective)
2. What type of data have they uploaded? (Understand the data structure — list, timeline, reviews, etc.)
3. What kind of analysis do they want? (See what happened, understand why, predict future, or suggest actions)
4. What numbers or facts matter most? (Key metrics or facts they want to track)
5. How do they want to see the information? (Charts, tables, timelines — visual preferences)
6. Do they want filters to focus on certain products, regions, or time periods?
7. Who will use this dashboard? (Just them, their team, their manager — audience matters)

Throughout, be respectful, collaborative, and approachable. Confirm your assumptions, explain why each question matters, and make sure the user feels confident that you understand their needs.
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
    
    # Add distribution insights
    for col, stats in distribution_summary.items():
        if 'mean' in stats:  # Numeric column
            insights.append(f"- {col}: Average {stats['mean']:.2f}, ranges from {stats['min']:.2f} to {stats['max']:.2f}")
        elif 'top_values' in stats:  # Categorical column
            top_vals = list(stats['top_values'].items())[:3]
            insights.append(f"- {col}: Most common values are {', '.join(f'{val} ({count})' for val, count in top_vals)}")
    
    # Add outlier insights
    for col, stats in outlier_report.items():
        if stats['outlier_count'] > 0:
            insights.append(f"- {col}: Contains {stats['outlier_count']} outliers")
    
    return "\n".join(insights)

def format_filter_suggestions(suggested_filters: list, date_frequencies: Dict[str, str]) -> str:
    """Format the filter suggestions into a readable summary"""
    suggestions = suggested_filters.copy()
    
    # Add date frequency information
    for col, freq in date_frequencies.items():
        if freq != "Irregular":
            suggestions.append(f"Time-based analysis possible on '{col}' ({freq} frequency)")
    
    return "\n".join(f"- {suggestion}" for suggestion in suggestions)

def generate_prompt_template(file_path: str) -> str:
    """Generate a complete prompt template with data analysis results"""
    # Process the data file
    context = process_file(file_path)
    
    # Format each section
    data_quality_summary = format_data_quality_summary(context['data_quality'])
    column_type_summary = format_column_type_summary(context['column_types'])
    data_insights = format_data_insights(
        context['basic_distribution_summary'],
        context['outlier_report']
    )
    filter_suggestions = format_filter_suggestions(
        context['suggested_filters'],
        context['date_frequencies']
    )
    
    # Get the base template and fill in the placeholders
    template = create_base_template()
    filled_template = template.format(
        data_quality_summary=data_quality_summary,
        column_type_summary=column_type_summary,
        data_insights=data_insights,
        filter_suggestions=filter_suggestions
    )
    
    return filled_template

if __name__ == "__main__":
    file_path = "example_data.csv"
    prompt = generate_prompt_template(file_path)
    print(prompt) 