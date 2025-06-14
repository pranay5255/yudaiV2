from typing import Any

def process_message(message: str) -> Any:
    return {"message": message}

def process_file(path: str) -> Any:
    return {"path": path}
