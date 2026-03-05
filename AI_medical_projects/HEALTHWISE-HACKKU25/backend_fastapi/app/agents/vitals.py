from typing import Any, Dict
from app.agents.base import BaseAgent

class VitalsAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="VitalsAgent")

    async def process(self, input_data: Any) -> Dict[str, Any]:
        # Logic: Check constants for vitals
        heart_rate = input_data.get('heart_rate', 0)
        sys_bp = input_data.get('sys_bp', 120)
        
        status = "Normal"
        if heart_rate > 100 or heart_rate < 60:
            status = "Abnormal Heart Rate"
            
        return {
            "agent": self.name,
            "analysis": f"Heart Rate: {heart_rate} bpm. Status: {status}",
            "alert": status != "Normal"
        }
