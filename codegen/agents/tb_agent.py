import json
import os
from typing import Dict, Any
import logging
from openai import OpenAI
from dotenv import load_dotenv
from app.context_manager import ContextManager

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TBAgent:
    """Agent responsible for generating code based on a data schema and a user prompt"""
    
    def __init__(self):
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        self.context_manager = ContextManager()
        self.system_message = {
            "role": "system",
            "content": """You are an expert data analyst. Your task is to generate Python code based on the provided data schema and user prompt.
            Follow these guidelines:
            1. Analyze the data schema carefully to understand the structure and types of data available
            2. Generate appropriate Python code that addresses the user's request
            3. Use pandas for data manipulation
            4. Include proper error handling
            5. Add comments explaining complex operations
            6. Return only executable Python code

            The response should be clean Python code without any additional text or markdown."""
        }

    def create_prompt(self, user_prompt: str) -> str:
        """Create a formatted prompt combining the data schema and user request"""
        # Get current dataset profile from context
        dataset_profile = self.context_manager.get_dataset_profile()
        if not dataset_profile:
            raise ValueError("No dataset profile found in context")

        return f"""
Data Schema:
{json.dumps(dataset_profile.dict(), indent=2)}

Previous User Inputs:
{json.dumps([input['input'] for input in self.context_manager.get_context()['user_inputs']], indent=2)}

Current User Request:
{user_prompt}

Generate Python code that accomplishes this task using the provided data schema.
"""

    def generate_code(self, user_prompt: str) -> str:
        """Generate code based on the data schema and user prompt"""
        try:
            # Add user input to context
            self.context_manager.add_user_input(user_prompt)
            
            formatted_prompt = self.create_prompt(user_prompt)
            
            response = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "", 
                    "X-Title": "",
                },
                model="qwen/qwq-32b:free",
                messages=[
                    self.system_message,
                    {"role": "user", "content": formatted_prompt}
                ],
                temperature=0.7,
                max_tokens=2048,
                top_p=1
            )
            
            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Error generating code: {str(e)}")
            raise

    def generate_profile_summary(self, profile_path: str) -> str:
        """Generate a complete summary of the dataset profile using OpenAI"""
        try:
            with open(profile_path, 'r') as f:
                profile_data = json.load(f)
            
            # Update context with profile data
            self.context_manager.update_dataset_profile(profile_data)
            
            return self.generate_code("Generate a summary of this dataset")

        except Exception as e:
            logger.error(f"Error generating profile summary: {str(e)}")
            raise

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        profiler = TBAgent()
        summary = profiler.generate_profile_summary(sys.argv[1])
        print(summary)
    else:
        print("Please provide a path to a profile JSON file") 