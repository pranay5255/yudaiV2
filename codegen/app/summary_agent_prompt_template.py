from typing import Dict, Any, List
import json
from app.models import DatasetProfile
from .context_manager import Context, ContextManager

def create_base_template() -> str:
    """Returns the enhanced summary agent template for ECharts configuration"""
    return '''
    You are a Dashboard Configuration Agent responsible for generating comprehensive ECharts configurations for interactive dashboards based on data analysis, historical context, and user requirements.

    Your task is to generate a detailed JSON configuration that defines 4 complementary chart components using ECharts. Each chart definition must include:

    Required Properties for each chart:
    {
        "chart_id": "unique_identifier",
        "chart_type": "One of: line, bar, pie, scatter, heatmap, radar, gauge, sunburst, tree, treemap, sankey, boxplot",
        "title": {
            "text": "Clear descriptive title",
            "left": "center/left/right"
        },
        "tooltip": {
            "trigger": "item/axis/none",
            "formatter": "string or function template"
        },
        "legend": {
            "data": ["series names"],
            "type": "plain/scroll",
            "orient": "horizontal/vertical",
            "position": "top/bottom/right"
        },
        "dataset": {
            "source": ["required_columns"],
            "dimensions": ["dimension", "names"]
        },
        "xAxis": {
            "type": "category/value/time",
            "name": "x axis name"
        },
        "yAxis": {
            "type": "value/category",
            "name": "y axis name"
        },
        "series": [{
            "type": "chart_type",
            "name": "series name",
            "encode": {
                "x": "x dimension name/index",
                "y": "y dimension name/index"
            },
            "emphasis": {
                "focus": "self/series"
            }
        }],
        "dataZoom": [{
            "type": "slider/inside",
            "orient": "horizontal/vertical"
        }],
        "toolbox": {
            "feature": {
                "dataZoom": {},
                "brush": {},
                "restore": {},
                "saveAsImage": {}
            }
        },
        "visualMap": {
            "type": "continuous/piecewise",
            "dimension": "dimension index"
        }
    }

    Dataset Profile:
    {dataset_profile}

    User Requirements from Conversation:
    {conversation_history}

    Generate exactly 4 complementary charts that:
    1. Address the user's specific requirements from the conversation
    2. Highlight key insights from the dataset profile
    3. Leverage ECharts' interactive features:
       - Zooming and scrolling with dataZoom
       - Rich tooltips with formatter
       - Linked chart interactions with emphasis
       - Visual mapping for data ranges
    4. Follow ECharts visualization best practices:
       - Responsive layouts
       - Proper axis and legend placement
       - Consistent color schemes
       - Clear data labels and tooltips

    Respond with a valid ECharts configuration containing exactly 4 charts.
    '''

def format_dataset_profile(profile: DatasetProfile) -> str:
    """Format the dataset profile into a readable summary"""
    if not profile:
        return "No dataset profile available"
        
    # Handle case where profile might be a dict
    if isinstance(profile, dict):
        profile = DatasetProfile(**profile)
        
    summary = [
        f"Dataset: {profile.analysis.title}",
        f"Rows: {profile.table.n:,}",
        f"Columns: {profile.table.n_var}",
        f"Date Range: {profile.analysis.date_start} to {profile.analysis.date_end}",
        f"Missing Data: {profile.table.p_cells_missing:.1%}",
        f"Duplicate Rows: {profile.table.n_duplicates:,}",
        "\nColumn Types:",
    ]
    
    for type_name, count in profile.table.types.items():
        summary.append(f"- {type_name}: {count}")
    
    summary.append("\nKey Variables:")
    for var_name, var_info in profile.variables.items():
        summary.append(f"- {var_name} ({var_info.type})")
        if var_info.type == "Numeric":
            summary.append(f"  Range: {var_info.range}")
        elif var_info.type == "Categorical":
            summary.append(f"  Unique Values: {var_info.n_unique}")
    
    return "\n".join(summary)

def format_conversation_history(context: Context) -> str:
    """Format the conversation history from context"""
    # Handle case where context might be a dict
    if isinstance(context, dict):
        context = Context(**context)
        
    history = []
    
    # Add session info
    if hasattr(context.session_info, 'created_at'):
        history.append(f"Session Started: {context.session_info.created_at}")
        history.append(f"Current Turn: {context.session_info.current_turn}\n")
    
    # Format user inputs with timestamps
    for input_entry in context.user_inputs:
        # Handle both dict and UserInput objects
        if isinstance(input_entry, dict):
            timestamp = input_entry.get('timestamp', 'N/A')
            input_text = input_entry.get('input', '')
            command = input_entry.get('command', None)
        else:
            timestamp = input_entry.timestamp
            input_text = input_entry.input
            command = input_entry.command
            
        history.append(f"User Input ({timestamp}):")
        history.append(f"  {input_text}")
        if command:
            history.append(f"  Command: {command}")
    
    # Format analysis results with timestamps and types
    for result in context.analysis_history:
        # Handle both dict and AnalysisResult objects
        if isinstance(result, dict):
            timestamp = result.get('timestamp', 'N/A')
            result_type = result.get('type', '')
            command = result.get('command', None)
            result_data = result.get('result', {})
        else:
            timestamp = result.timestamp
            result_type = result.type
            command = result.command
            result_data = result.result
            
        history.append(f"\nAnalysis Result ({timestamp}):")
        history.append(f"Type: {result_type}")
        if command:
            history.append(f"Command: {command}")
        
        if isinstance(result_data, dict):
            for key, value in result_data.items():
                history.append(f"- {key}: {value}")
    
    return "\n".join(history)

def generate_chart_prompt_template(profile: DatasetProfile, context: Context) -> str:
    """Generate a complete prompt template with dataset profile and conversation history"""
    template = create_base_template()
    
    # Validate that we have required data
    if not profile or not context:
        raise ValueError("Both profile and context are required to generate the prompt template")
    
    # Handle dict inputs
    if isinstance(context, dict):
        context = Context(**context)
    if isinstance(profile, dict):
        profile = DatasetProfile(**profile)
    
    # Check if conversation is complete
    if context.session_info.conversation_complete:
        template += "\nNote: This is a completed conversation. No further updates should be made."
    
    return template.format(
        dataset_profile=format_dataset_profile(profile),
        conversation_history=format_conversation_history(context)
    )

def parse_llm_response(response: str) -> Dict:
    """Parse the LLM response to extract the JSON configuration"""
    try:
        # First try to parse the entire response as JSON
        return json.loads(response)
    except json.JSONDecodeError:
        # Try to extract JSON from markdown code blocks
        import re
        json_match = re.search(r'```(?:json)?\n(.*?)\n```', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Try to extract anything that looks like JSON
        json_match = re.search(r'({[\s\S]*})', response)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        return {}

def example_chart_config() -> Dict:
    """Returns an example ECharts configuration with exactly 4 charts"""
    return {
        "dashboard_config": {
            "title": "Data Analysis Dashboard",
            "description": "Interactive dashboard showing key insights from the dataset",
            "theme": "light",
            "charts": [
                {
                    "chart_id": "time_series_trend",
                    "chart_type": "line",
                    "title": {
                        "text": "Temporal Trend Analysis",
                        "left": "center"
                    },
                    "tooltip": {
                        "trigger": "axis",
                        "axisPointer": {
                            "type": "cross"
                        }
                    },
                    "legend": {
                        "data": ["Value"],
                        "type": "scroll",
                        "bottom": 0
                    },
                    "dataset": {
                        "source": [["timestamp", "value"]],
                        "dimensions": ["timestamp", "value"]
                    },
                    "xAxis": {
                        "type": "time",
                        "name": "Date"
                    },
                    "yAxis": {
                        "type": "value",
                        "name": "Value"
                    },
                    "series": [{
                        "type": "line",
                        "name": "Value",
                        "encode": {
                            "x": "timestamp",
                            "y": "value"
                        },
                        "emphasis": {
                            "focus": "series"
                        }
                    }],
                    "dataZoom": [{
                        "type": "slider",
                        "show": true,
                        "bottom": 30
                    }, {
                        "type": "inside"
                    }],
                    "toolbox": {
                        "feature": {
                            "dataZoom": {},
                            "restore": {},
                            "saveAsImage": {}
                        }
                    }
                },
                # ... 3 more chart configurations with similar structure ...
            ]
        }
    }

if __name__ == "__main__":
    # Example usage with new context management system
    context_manager = ContextManager()
    
    # Add some mock data for testing
    context_manager.add_mock_entries()
    
    # Get the profile and context
    profile = context_manager.get_dataset_profile()
    context = Context(**context_manager.get_context())
    
    if profile:
        try:
            prompt = generate_chart_prompt_template(profile, context)
            print(prompt)
            
            print("\nExample output configuration:")
            print(json.dumps(example_chart_config(), indent=2))
        except Exception as e:
            print(f"Error generating prompt template: {e}")
    else:
        print("No dataset profile available. Please upload a dataset first.") 