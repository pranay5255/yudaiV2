import os
from typing import Dict, Any, Tuple
import logging
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InsightGenAgent:
    """Agent responsible for generating insights and questions based on dataset profile summaries"""
    
    def __init__(self):
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        self.system_message = {
            "role": "system",
            "content": """You are an expert data analyst. Your task is to:
            1. Generate ONE meaningful insight from the dataset profile summary
            2. Choose ONE relevant question from this list of critical questions:
               - What is the main goal of the dashboard? (Understand their objective)
               - What type of data have they uploaded? (Understand the data structure — list, timeline, reviews, etc.)
               - What kind of analysis do they want? (See what happened, understand why, predict future, or suggest actions)
               - What numbers or facts matter most? (Key metrics or facts they want to track)
               - How do they want to see the information? (Charts, tables, timelines — visual preferences)
               - Do they want filters to focus on certain products, regions, or time periods?
               - Who will use this dashboard? (Just them, their team, their manager — audience matters)
            
            The question you choose should be relevant to the insight you generate.
            
            Format your response EXACTLY as:
            INSIGHT: <your insight>
            QUESTION: <selected question>"""
        }

    def generate_insight_and_question(self, profile_summary: str) -> Tuple[str, str]:
        """Generate an insight and a relevant question using OpenAI"""
        try:
            # Create user message with the profile summary
            user_message = {
                "role": "user",
                "content": f"Based on this dataset profile summary, generate one insight and choose one relevant question:\n\n{profile_summary}"
            }
            
            # Call OpenAI API with proper message structure
            response = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://github.com/yudai-data-analysis", 
                    "X-Title": "Yudai Data Analysis",
                },
                model="openai/gpt-4",
                messages=[
                    self.system_message,
                    user_message
                ],
                temperature=0.6,
                max_tokens=2048,
                top_p=1
            )
            
            # Parse response
            content = response.choices[0].message.content
            insight_line = next(line for line in content.split('\n') if line.startswith('INSIGHT:'))
            question_line = next(line for line in content.split('\n') if line.startswith('QUESTION:'))
            
            insight = insight_line.replace('INSIGHT:', '').strip()
            question = question_line.replace('QUESTION:', '').strip()
            
            return insight, question

        except Exception as e:
            logger.error(f"Error generating insight and question: {str(e)}")
            raise

if __name__ == "__main__":
    # Example usage
    example_summary = """
    Dataset Analysis:
    - Time Range: 2023-01-01 to 2023-12-31
    - Total Observations: 1000
    
    Table Statistics:
    - Column Types:
      * Numeric: 5
      * DateTime: 2
      * Categorical: 3
    """
    
    agent = InsightGenAgent()
    insight, question = agent.generate_insight_and_question(example_summary)
    print(f"Insight: {insight}")
    print(f"Question: {question}") 