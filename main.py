import uvicorn
from codegen.api.chat import app

# Placeholder message handlers used by FastAPI endpoints
def process_message(message: str):
    return {"message": message}

def process_file(path: str):
    return {"path": path}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
