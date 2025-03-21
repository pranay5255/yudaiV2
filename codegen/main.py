from typing import Dict, Any
import json
import os
import logging
from datetime import datetime
from app.context_manager import ContextManager
from agents.tb_agent import TBAgent
from agents.base_eda import process_file

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize global instances
context_manager = ContextManager()
tb_agent = TBAgent()

def process_message(message: str) -> Dict[str, Any]:
    """Process incoming messages and generate code"""
    try:
        logger.info(f"Processing message: {message}")
        
        # Generate code using TB agent
        code = tb_agent.generate_code(message)
        
        return {
            "message": "Code generated successfully",
            "code": code
        }
        
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        raise

def process_file(file_path: str) -> Dict[str, Any]:
    """Process uploaded file and initialize analysis"""
    try:
        logger.info(f"Processing file: {file_path}")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Generate initial profile
        eda_results = process_file(file_path)
        
        # Update context with dataset metadata
        metadata = {
            "file_path": file_path,
            "column_types": eda_results.get('column_types', {}),
            "data_quality": eda_results.get('data_quality', {}),
            "timestamp": datetime.now().isoformat()
        }
        
        context_manager.update_dataset_metadata(metadata)
        context_manager.update_dataset_profile(eda_results)
        
        return eda_results
        
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise

def generate_dashboard_prompt(file_path: str, user_prompt: str) -> str:
    """Generate a prompt for dashboard configuration"""
    try:
        # Add user input to context
        context_manager.add_user_input(user_prompt)
        
        # Get current dataset profile
        profile = context_manager.get_dataset_profile()
        if not profile:
            raise ValueError("No dataset profile found")
            
        return f"""
Based on the dataset with the following characteristics:
- Columns: {', '.join(profile.get('columns', []))}
- Data Quality: {json.dumps(profile.get('data_quality', {}), indent=2)}

User Request: {user_prompt}

Generate a dashboard configuration that addresses this request.
"""
    except Exception as e:
        logger.error(f"Error generating dashboard prompt: {str(e)}")
        raise

if __name__ == "__main__":
    # Example usage
    try:
        # Process a sample file
        sample_data_path = "sample_data.csv"
        if os.path.exists(sample_data_path):
            results = process_file(sample_data_path)
            print("File processed successfully")
            
            # Process a sample message
            response = process_message("Generate code to analyze the data")
            print("Message processed successfully")
            print(f"Generated code:\n{response['code']}")
            
    except Exception as e:
        print(f"Error in main: {str(e)}")
