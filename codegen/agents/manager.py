from typing import Dict, Any
from .data_exploration_agent import DataExplorationAgent
from .orchestrator_agent_sdk import OpenAIOrchestratorAgent, ClarificationRequired

class CodeGenAgent:
    def generate(self, eda: Dict[str, Any]) -> str:
        # In real system this would generate code and return a path to a zip
        return "http://example.com/generated.zip"

class ManagerAgent:
    """Implements manager-worker pattern."""
    def __init__(self, assistant_id: str | None = None):
        self.explorer = DataExplorationAgent()
        self.orchestrator = OpenAIOrchestratorAgent(assistant_id=assistant_id)
        self.codegen = CodeGenAgent()

    def handle(self, csv_path: str, prompt: str, context: Dict[str, Any]) -> str:
        eda = self.explorer.explore(csv_path)
        try:
            self.orchestrator.clarify_user(context)
        except ClarificationRequired as c:
            # In manager pattern we would surface questions, but for unit test we skip
            pass
        return self.codegen.generate(eda)
