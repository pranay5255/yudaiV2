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
    current_turn: int = 1
    conversation_complete: bool = False

class Context(BaseModel):
    session_info: SessionInfo
    dataset_profile: DatasetProfile | None = None
    user_inputs: List[UserInput] = []
    analysis_history: List[AnalysisResult] = []

class ContextManager:
    def __init__(self, context_file_path: str = "session_context.json", markdown_path: str = "contextFile.md"):
        self.context_file_path = context_file_path
        self.markdown_path = markdown_path
        self.context = self._initialize_context()
        self._initialize_markdown()

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
            user_inputs=[],
            analysis_history=[]
        ).dict()

    def _initialize_markdown(self) -> None:
        """Initialize or create the markdown context file"""
        if not os.path.exists(self.markdown_path):
            with open(self.markdown_path, 'w') as f:
                f.write("# Analysis Session Context\n\n")
                f.write("## Dataset Information\n")
                f.write("*No dataset uploaded yet*\n\n")
                f.write("## Conversation History\n\n")

    def update_dataset_profile(self, profile: Dict[str, Any]) -> None:
        """Update dataset profile in context and markdown"""
        validated_profile = DatasetProfile(**profile)
        self.context["dataset_profile"] = validated_profile.dict()
        self.context["session_info"]["last_updated"] = datetime.now().isoformat()
        self.context["session_info"]["dataset_name"] = validated_profile.analysis.title
        
        # Update markdown with dataset information
        self._update_markdown_dataset_info(validated_profile)
        self._save_context()

    def add_user_input(self, user_input: str, command: str | None = None) -> None:
        """Add user input to context and markdown"""
        input_entry = UserInput(
            timestamp=datetime.now(),
            input=user_input,
            command=command
        )
        self.context["user_inputs"].append(input_entry.dict())
        
        # Update markdown with user input
        self._append_to_markdown(f"\n### User Input (Turn {self.context['session_info']['current_turn']})\n")
        self._append_to_markdown(f"```\n{user_input}\n```\n")
        
        self._save_context()

    def add_analysis_result(self, result_type: str, analysis: Dict[str, Any], command: str | None = None) -> None:
        """Add analysis result to context and markdown"""
        result_entry = AnalysisResult(
            timestamp=datetime.now(),
            type=result_type,
            result=analysis,
            command=command
        )
        self.context["analysis_history"].append(result_entry.dict())
        
        # Update markdown with analysis result
        self._append_to_markdown(f"\n### Analysis Result (Turn {self.context['session_info']['current_turn']})\n")
        self._append_to_markdown(f"Type: {result_type}\n")
        self._append_to_markdown("```json\n" + json.dumps(analysis, indent=2) + "\n```\n")
        
        self._save_context()

    def advance_turn(self) -> None:
        """Advance to the next conversation turn"""
        current_turn = self.context["session_info"]["current_turn"]
        if current_turn < 2:
            self.context["session_info"]["current_turn"] = current_turn + 1
        else:
            self.context["session_info"]["conversation_complete"] = True
        self._save_context()

    def get_current_turn(self) -> int:
        """Get the current conversation turn"""
        return self.context["session_info"]["current_turn"]

    def is_conversation_complete(self) -> bool:
        """Check if the conversation is complete"""
        return self.context["session_info"]["conversation_complete"]

    def _update_markdown_dataset_info(self, profile: DatasetProfile) -> None:
        """Update the dataset information section in markdown"""
        dataset_info = [
            "## Dataset Information\n",
            f"- **Name**: {profile.analysis.title}",
            f"- **Rows**: {profile.table.n:,}",
            f"- **Columns**: {profile.table.n_var}",
            f"- **Time Range**: {profile.analysis.date_start} to {profile.analysis.date_end}",
            f"- **Missing Data**: {profile.table.p_cells_missing:.1%}",
            f"- **Duplicate Rows**: {profile.table.n_duplicates:,}",
            "\n### Column Types",
        ]
        
        for type_name, count in profile.table.types.items():
            dataset_info.append(f"- {type_name}: {count}")
        
        # Replace the existing dataset information section
        with open(self.markdown_path, 'r') as f:
            content = f.read()
            start_idx = content.find("## Dataset Information")
            end_idx = content.find("## Conversation History")
            
        if start_idx != -1 and end_idx != -1:
            new_content = content[:start_idx] + "\n".join(dataset_info) + "\n\n" + content[end_idx:]
            with open(self.markdown_path, 'w') as f:
                f.write(new_content)

    def _append_to_markdown(self, text: str) -> None:
        """Append text to the markdown file"""
        with open(self.markdown_path, 'a') as f:
            f.write(text)

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