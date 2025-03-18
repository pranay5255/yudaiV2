from typing import Dict, Any
import json
import os
from datetime import datetime
from pydantic import BaseModel
from app.models import DatasetProfile

class UserInput(BaseModel):
    timestamp: datetime
    input: str

class SessionInfo(BaseModel):
    created_at: datetime
    last_updated: datetime
    dataset_name: str | None = None

class Context(BaseModel):
    session_info: SessionInfo
    dataset_profile: DatasetProfile | None = None
    user_inputs: list[UserInput] = []

class ContextManager:
    def __init__(self, context_file_path: str = "session_context.json"):
        self.context_file_path = context_file_path
        self.context = self._initialize_context()

    def _initialize_context(self) -> Dict[str, Any]:
        """Initialize or load existing context"""
        if os.path.exists(self.context_file_path):
            with open(self.context_file_path, 'r') as f:
                context_data = json.load(f)
                return Context(**context_data).dict()
        
        return Context(
            session_info=SessionInfo(
                created_at=datetime.now(),
                last_updated=datetime.now()
            ),
            dataset_profile=None,
            user_inputs=[]
        ).dict()

    def update_dataset_profile(self, profile: Dict[str, Any]) -> None:
        """Update dataset profile in context"""
        validated_profile = DatasetProfile(**profile)
        self.context["dataset_profile"] = validated_profile.dict()
        self.context["session_info"]["last_updated"] = datetime.now().isoformat()
        self.context["session_info"]["dataset_name"] = validated_profile.analysis.title
        self._save_context()

    def add_user_input(self, user_input: str) -> None:
        """Add user input to context"""
        input_entry = UserInput(
            timestamp=datetime.now(),
            input=user_input
        )
        self.context["user_inputs"].append(input_entry.dict())
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
        validated_context = Context(**self.context)
        with open(self.context_file_path, 'w') as f:
            json.dump(validated_context.dict(), f, indent=2, default=str)

    def add_mock_entries(self) -> None:
        """Add mock user inputs and analysis results for testing"""
        # Mock user inputs
        self.add_user_input(
            "I need a dashboard to track our e-commerce sales performance"
        )
        
        self.add_user_input(
            "Show me the sales trends over time and by product category"
        )
        
        # Mock analysis results
        self.add_analysis_result(
            "sales_overview",
            {
                "total_sales": 150000,
                "avg_order_value": 250,
                "top_category": "Electronics"
            },
            command="sales_analysis"
        )
        
        self.add_analysis_result(
            "trend_analysis",
            {
                "growth_rate": "15%",
                "peak_month": "December",
                "trending_products": ["Laptops", "Smartphones"]
            },
            command="trend_analysis"
        )