import os
from typing import Dict, List, Any
from openai import OpenAI

class ClarificationRequired(Exception):
    """Raised when the user must clarify missing fields."""
    def __init__(self, questions: List[str]):
        self.questions = questions
        super().__init__("Clarification required")

class OpenAIOrchestratorAgent:
    """Minimal orchestrator using OpenAI Assistants API."""

    def __init__(self, assistant_id: str | None = None):
        api_key = os.getenv("OPENROUTER_API_KEY")
        if api_key:
            self.client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
        else:
            self.client = None
        self.assistant_id = assistant_id

    def clarify_user(self, values: Dict[str, Any]) -> None:
        """If any value is missing, raise ClarificationRequired with 7 questions."""
        missing = [k for k, v in values.items() if v in (None, "")]
        if missing:
            questions = [f"Please provide value for {field}?" for field in missing][:7]
            if len(questions) < 7:
                questions += ["Could you elaborate further?"] * (7 - len(questions))
            raise ClarificationRequired(questions)

    def run(self, message: str, context: Dict[str, Any]) -> str:
        """Send a message via Assistant."""
        self.clarify_user(context)
        if not self.client:
            return "no-op"
        thread = self.client.beta.threads.create(messages=[{"role": "user", "content": message}])
        run = self.client.beta.threads.runs.create(thread_id=thread.id, assistant_id=self.assistant_id)
        run = self.client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        return run.status
