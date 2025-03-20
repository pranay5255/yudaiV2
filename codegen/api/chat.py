from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional
import logging
from ..main import process_message, process_file

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    message: str

class MessageResponse(BaseModel):
    message: str
    code: Optional[str] = None

@app.post("/chat/message", response_model=MessageResponse)
async def handle_message(request: MessageRequest):
    """Handle incoming chat messages"""
    try:
        # Process message using main module
        result = process_message(request.message)
        return MessageResponse(**result)
        
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def handle_file_upload(file_path: str):
    """Handle file uploads"""
    try:
        # Process file using main module
        result = process_file(file_path)
        return {"success": True, "data": result}
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
