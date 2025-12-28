import os
import json
import time
import re

class DebateLogger:
    def __init__(self, log_dir="logs"):
        """
        Initializes the logger. Creates the directory if it doesn't exist
        and sets up a unique filename based on the timestamp.
        """
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        self.filepath = f"{log_dir}/debate_log_{int(time.time())}.json"
        print(f"DEBUG: Logging initialized at {self.filepath}")

    def log(self, event_type: str, data: dict):
        """
        Appends a single event to the JSON log file.
        """
        entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "event_type": event_type,
            "data": self._serialize(data)
        }
        
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def _serialize(self, data):
        """
        Helper to ensure non-JSON-serializable objects (like LangChain Messages)
        are converted to strings so the logger doesn't crash.
        """
        if hasattr(data, "content"):  # Handle LangChain Message objects
            return data.content
        if hasattr(data, "dict"):     # Handle Pydantic models
            return data.dict()
        return str(data)

def validate_topic(topic: str) -> str:
    """
    Sanitizes and validates the user input topic.
    Raises ValueError if invalid.
    """
    # Remove special chars that might mess up prompts, keep alphanumeric + basic punctuation
    sanitized = re.sub(r'[^\w\s\?\.\,\-]', '', topic).strip()
    
    if len(sanitized) < 5:
        raise ValueError("Topic is too short (min 5 characters).")
    
    if len(sanitized) > 100:
        raise ValueError("Topic is too long (max 100 characters).")
        
    return sanitized