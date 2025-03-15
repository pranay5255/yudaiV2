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
from models import DatasetProfile

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
            profile = ProfileReport(df, title=dataset_name)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{dataset_name}_{timestamp}_profile.json"
            filepath = self.upload_dir / filename

            print(f"Profile saved to: {filepath}")

            # Save profile to JSON string first
            json_data = profile.to_json()
            
            # Then write it to file
            with open(filepath, 'w') as f:
                f.write(json_data)
            
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
