import json
import os
from typing import Dict, Any
import logging
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatasetProfilerAgent:
    """Agent responsible for analyzing and summarizing dataset profile information"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)
        self.system_message = {
            "role": "system",
            "content": """You are a data profiling expert. Your task is to analyze JSON profile data and extract key insights.
            Focus on these aspects in your analysis:
            1. Dataset Overview - time range and total observations
            2. Time Series Characteristics - any seasonal patterns or frequency
            3. Data Quality - missing values, duplicates, outliers
            4. Variable Analysis - key columns and their distributions
            5. Relationships - notable correlations or patterns
            6. Potential Issues - data quality alerts or concerns
            
            Format your response as a clear, structured summary with sections."""
        }

    def generate_profile_summary(self, profile_path: str) -> str:
        """Generate a complete summary of the dataset profile using OpenAI"""
        try:
            # Load profile data
            with open(profile_path, 'r') as f:
                profile_data = json.load(f)
            
            
            # Create user message with the profile data
            user_message = {
                "role": "user", 
                "content": f"Please analyze this dataset profile and provide a structured summary:\n{json.dumps(profile_data, indent=2)}"
            }
            
            # Call OpenAI API with proper message structure
            response = self.client.responses.create(
                model="gpt-4o-mini",
                input=[{
                    "role": "system",
                    "content": self.system_message["content"]
                }, {
                    "role": "user",
                    "content": user_message["content"]
                }],
                text={
                    "format": {
                        "type": "text"
                    }
                },
                reasoning={},
                tools=[],
                temperature=0.6,
                max_output_tokens=2048,
                top_p=1,
                store=True
            )
            
            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error generating profile summary: {str(e)}")
            raise

    

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        profiler = DatasetProfilerAgent()
        summary = profiler.generate_profile_summary(sys.argv[1])
        print(summary)
    else:
        print("Please provide a path to a profile JSON file") 