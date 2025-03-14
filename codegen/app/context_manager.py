from typing import Dict, Any, List
import json
import os
from datetime import datetime
from pydantic import BaseModel
from models import DatasetProfile

class UserInput(BaseModel):
    timestamp: datetime
    input: str
    command: str | None = None

class AnalysisResult(BaseModel):
    timestamp: datetime
    type: str
    result: Dict[str, Any]
    command: str | None = None

class SessionInfo(BaseModel):
    created_at: datetime
    last_updated: datetime
    dataset_name: str | None = None

class Context(BaseModel):
    session_info: SessionInfo
    dataset_profile: DatasetProfile | None = None
    user_inputs: List[UserInput] = []
    analysis_history: List[AnalysisResult] = []

class ContextManager:
    def __init__(self, context_file_path: str = "session_context.json"):
        self.context_file_path = context_file_path
        self.context = self._initialize_context()

    def _initialize_context(self) -> Dict[str, Any]:
        """Initialize or load existing context"""
        if os.path.exists(self.context_file_path):
            with open(self.context_file_path, 'r') as f:
                context_data = json.load(f)
                # Validate context with Pydantic
                return Context(**context_data).dict()
        
        return Context(
            session_info=SessionInfo(
                created_at=datetime.now(),
                last_updated=datetime.now()
            ),
            dataset_profile=None,
            user_inputs=[],
            analysis_history=[]
        ).dict()

    def update_dataset_profile(self, profile: Dict[str, Any]) -> None:
        """Update dataset profile in context"""
        # Validate profile using DatasetProfile model
        validated_profile = DatasetProfile(**profile)
        self.context["dataset_profile"] = validated_profile.dict()
        self.context["session_info"]["last_updated"] = datetime.now().isoformat()
        self.context["session_info"]["dataset_name"] = validated_profile.analysis.title
        self._save_context()

    def add_user_input(self, user_input: str, command: str | None = None) -> None:
        """Add user input to context history"""
        input_entry = UserInput(
            timestamp=datetime.now(),
            input=user_input,
            command=command
        )
        self.context["user_inputs"].append(input_entry.dict())
        self._save_context()

    def add_analysis_result(self, result_type: str, analysis: Dict[str, Any], command: str | None = None) -> None:
        """Add analysis result to context history"""
        result_entry = AnalysisResult(
            timestamp=datetime.now(),
            type=result_type,
            result=analysis,
            command=command
        )
        self.context["analysis_history"].append(result_entry.dict())
        self._save_context()

    def get_context(self) -> Dict[str, Any]:
        """Get current context"""
        return self.context

    def get_dataset_profile(self) -> DatasetProfile | None:
        """Get current dataset profile"""
        if self.context["dataset_profile"]:
            return DatasetProfile(**self.context["dataset_profile"])
        return None

    def _save_context(self) -> None:
        """Save context to file with validation"""
        # Validate entire context before saving
        validated_context = Context(**self.context)
        with open(self.context_file_path, 'w') as f:
            json.dump(validated_context.dict(), f, indent=2, default=str)