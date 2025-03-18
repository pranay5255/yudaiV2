from typing import Dict, Any, List, Tuple
from app.models import DatasetProfile
from datetime import datetime
from .insight_gen_agent import InsightGenAgent
from app.context_manager import ContextManager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Orchestrator:
    """Agent responsible for orchestrating conversations with users about their dashboard needs"""
    
    def __init__(self, context_manager: ContextManager):
        """Initialize the orchestrator with a context manager"""
        self.context_manager = context_manager
        self.insight_agent = InsightGenAgent()
        self.current_turn = 0
        self.insights = []
        self.questions = []
        
    def initialize_conversation(self, profile: DatasetProfile) -> str:
        """Initialize the conversation by getting insights and questions"""
        try:
            # Get insights and questions from insight agent
            self.insights, self.questions = self.insight_agent.generate_insight_and_question(profile)
            
            # Start first turn of conversation
            return self._format_turn_message(0)
            
        except Exception as e:
            logger.error(f"Error initializing conversation: {str(e)}")
            raise
            
    def process_response(self, user_response: str) -> str:
        """Process user's response and get next turn"""
        try:
            # Store user's response
            self.context_manager.add_user_input(user_response)
            
            # Move to next turn
            self.current_turn += 1
            
            # If we still have turns left
            if self.current_turn < 3:
                return self._format_turn_message(self.current_turn)
            
            # If we're done with all turns
            return "Thank you for your responses! Would you like me to generate a dashboard configuration based on our discussion?"
            
        except Exception as e:
            logger.error(f"Error processing response: {str(e)}")
            raise
            
    def _format_turn_message(self, turn_index: int) -> str:
        """Format the message for a given turn"""
        return f"""
Here's what I found in your data:
{self.insights[turn_index]}

{self.questions[turn_index]}
"""

if __name__ == "__main__":
    # Example usage
    import sys
    import json
    
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            profile_data = json.load(f)
            profile = DatasetProfile(**profile_data)
            context_manager = ContextManager()
            orchestrator = Orchestrator(context_manager)
            print(orchestrator.initialize_conversation(profile))
    else:
        print("Please provide a path to a profile JSON file") 