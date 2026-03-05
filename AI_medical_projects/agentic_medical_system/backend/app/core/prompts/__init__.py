import os
from datetime import datetime
from app.core.config import settings

def load_system_prompt(**kwargs) -> str:
    prompt_path = os.path.join(os.path.dirname(__file__), "system.md")
    
    with open(prompt_path, "r") as f:
        return f.read().format(
            current_date_and_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **kwargs, 
        )
