from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional
from uuid import uuid4
import logging
from ..agents.prompt_template_orchestrator import Orchestrator
from app.models import DatasetProfile
from app.context_manager import ContextManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active conversations
conversations: Dict[str, Orchestrator] = {}

class InitializeRequest(BaseModel):
    profile: DatasetProfile

class MessageRequest(BaseModel):
    message: str

class ConversationResponse(BaseModel):
    message: str
    session_id: str
    done: bool = False

def get_session_orchestrator(session_id: str) -> Orchestrator:
    """Get the orchestrator for a given session ID"""
    if session_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversations[session_id]

@app.post("/chat/initialize", response_model=ConversationResponse)
async def initialize_conversation(request: InitializeRequest):
    """Initialize a new conversation with a dataset profile"""
    try:
        # Create a new session
        session_id = str(uuid4())
        
        # Initialize context manager and orchestrator
        context_manager = ContextManager()
        orchestrator = Orchestrator(context_manager)
        
        # Store orchestrator instance
        conversations[session_id] = orchestrator
        
        # Initialize conversation
        initial_message = orchestrator.initialize_conversation(request.profile)
        
        return ConversationResponse(
            message=initial_message,
            session_id=session_id
        )
    except Exception as e:
        logger.error(f"Error initializing conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/{session_id}/message", response_model=ConversationResponse)
async def process_message(
    session_id: str,
    request: MessageRequest,
    orchestrator: Orchestrator = Depends(get_session_orchestrator)
):
    """Process a message in an existing conversation"""
    try:
        # Process the message
        response = orchestrator.process_response(request.message)
        
        # Check if this is the final turn (after 3 turns)
        done = "Would you like me to generate a dashboard configuration" in response
        
        return ConversationResponse(
            message=response,
            session_id=session_id,
            done=done
        )
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/chat/{session_id}")
async def end_conversation(session_id: str):
    """End and cleanup a conversation"""
    try:
        if session_id in conversations:
            del conversations[session_id]
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error ending conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
