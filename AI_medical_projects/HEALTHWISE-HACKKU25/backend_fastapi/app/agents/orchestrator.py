from typing import Any, Dict
from app.agents.vitals import VitalsAgent
from app.agents.nutrition import NutritionAgent

class AgentOrchestrator:
    def __init__(self):
        self.agents = {
            "vitals": VitalsAgent(),
            "nutrition": NutritionAgent()
        }

    async def route_request(self, agent_name: str, data: Any) -> Dict[str, Any]:
        agent = self.agents.get(agent_name)
        if not agent:
            return {"error": "Agent not found"}
        
        return await agent.process(data)
        
orchestrator = AgentOrchestrator()
