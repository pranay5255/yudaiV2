from typing import Dict, Any
import json
import os
from datetime import datetime

class ContextManager:
    def __init__(self, context_file_path: str = "session_context.json"):
        self.context_file_path = context_file_path
        self.context = self._initialize_context()

    def _initialize_context(self) -> Dict[str, Any]:
        """Initialize or load existing context"""
        if os.path.exists(self.context_file_path):
            with open(self.context_file_path, 'r') as f:
                return json.load(f)
        return {
            "session_info": {
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            },
            "dataset_metadata": {},
            "user_inputs": [],
            "analysis_history": []
        }

    def update_dataset_metadata(self, metadata: Dict[str, Any]) -> None:
        """Update dataset metadata in context"""
        self.context["dataset_metadata"] = metadata
        self.context["session_info"]["last_updated"] = datetime.now().isoformat()
        self._save_context()

    def add_user_input(self, user_input: str) -> None:
        """Add user input to context history"""
        self.context["user_inputs"].append({
            "timestamp": datetime.now().isoformat(),
            "input": user_input
        })
        self._save_context()

    def add_analysis_result(self, analysis: Dict[str, Any]) -> None:
        """Add analysis result to context history"""
        self.context["analysis_history"].append({
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis
        })
        self._save_context()

    def get_context(self) -> Dict[str, Any]:
        """Get current context"""
        return self.context

    def _save_context(self) -> None:
        """Save context to file"""
        with open(self.context_file_path, 'w') as f:
            json.dump(self.context, f, indent=2)