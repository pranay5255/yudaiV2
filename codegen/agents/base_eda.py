import pandas as pd
import numpy as np
from typing import Dict, Any
from pathlib import Path
import json
import argparse
import sys
import os
from datetime import datetime
from ydata_profiling import ProfileReport
import logging
# from models import DatasetProfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProfiler:
    def __init__(self, upload_dir: str = "uploads/"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def load_data(self, file_path: str) -> pd.DataFrame:
        """Load data from various file formats"""
        try:
            if file_path.endswith('.csv'):
                return pd.read_csv(file_path)
            elif file_path.endswith(('.xls', '.xlsx')):
                return pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file format")
        except Exception as e:
            logger.error(f"Error loading file: {str(e)}")
            raise

    def generate_profile(self, df: pd.DataFrame, dataset_name: str) -> Dict[str, Any]:
        """Generate profile using YData Profiling"""

        
        try:
            # Create YData profile
            profile = ProfileReport(df,title=dataset_name,config_file='/home/pranay5255/Documents/yudaiV2/yudaiv2/codegen/agents/config.yml')
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{dataset_name}_{timestamp}_profile.json"
            filepath = self.upload_dir / filename

            print(f"Profile saved to: {filepath}")

            # Get profile as JSON data
            str_data = profile.to_json()
            
            # Convert string to JSON if needed
            if isinstance(str_data, str):
                json_data = json.loads(str_data)

            print([x for x in json_data['variables']])

            # Clean the profile data
            cleaned_data = clean_profile_data(json_data)
            
            # Write cleaned JSON to file
            with open(filepath, 'w') as f:
                json.dump(cleaned_data, f, indent=2)
            
            return str(filepath)

        except Exception as e:
            logger.error(f"Error generating profile: {str(e)}")
            raise

   

    def process_file(self, file_path: str) -> Dict[str, Any]:
        """Main processing pipeline"""
        try:
            dataset_name = Path(file_path).stem
            df = self.load_data(file_path)
            profile_path = self.generate_profile(df, dataset_name)
            
            
            logger.info(f"Profile saved to: {profile_path}")
            return profile_path

        except Exception as e:
            logger.error(f"Error in processing pipeline: {str(e)}")
            raise


def clean_profile_data(profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean the profile data by removing specified keys at top level and within variables.
        Also truncates dictionaries with more than 100 elements to first 10 elements in variables.
        
        Args:
            profile_data: The original profile data dictionary
            
        Returns:
            Dict[str, Any]: Cleaned profile data with specified keys removed and large dicts truncated
        """
        # Keys to remove at the top level
        keys_to_remove = ["missing", "package", "sample","duplicates"]
        
        # Keys to remove from within variables if present
        variable_keys_to_remove = [
            "value_counts_index_sorted",
            "value_counts_without_nan", 
            "histogram",
            # "length_histogram",
            # "histogram_length",
            # "character_counts",
            # "category_alias_values",
            # "block_alias_values",
            # "block_alias_counts",
            "n_block_alias",
            "block_alias_char_counts",
            "script_counts",
            "n_scripts",
            "script_char_counts",
            "category_alias_counts",
            "n_category",
            "category_alias_char_counts",
            "n_characters"
        ]
        
        # First clean the top level
        cleaned_data = {k: v for k, v in profile_data.items() if k not in keys_to_remove}
        
        # Clean the variables section if it exists
        if "variables" in cleaned_data and isinstance(cleaned_data["variables"], dict):
            for var_name, var_data in cleaned_data["variables"].items():
                if isinstance(var_data, dict):
                    # First filter out keys to remove
                    filtered_dict = {k: v for k, v in var_data.items() 
                                  if k not in variable_keys_to_remove}
                    
                    # Then check each remaining value and truncate if dictionary > 100 elements
                    truncated_dict = {}
                    for k, v in filtered_dict.items():
                        if isinstance(v, dict) and len(v) > 100:
                            # Take first 10 items
                            truncated_dict[k] = dict(list(v.items())[:10])
                        else:
                            truncated_dict[k] = v
                            
                    cleaned_data["variables"][var_name] = truncated_dict
        
        return cleaned_data

def main():
    parser = argparse.ArgumentParser(description='Generate dataset profile using YData Profiling.')
    parser.add_argument('input_file', help='Path to the input data file')
    
    args = parser.parse_args()
    
    try:
        profiler = DataProfiler()
        profile_data = profiler.process_file(args.input_file)
        print(json.dumps(profile_data, indent=2, default=str))
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
