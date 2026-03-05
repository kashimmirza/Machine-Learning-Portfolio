from typing import Any, Dict, List
from app.agents.base import BaseAgent
from app.agents.vitals import VitalsAgent
from app.agents.nutrition import NutritionAgent
from app.core.logging import logger
import asyncio

class AgentOrchestrator:
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {
            "vitals": VitalsAgent(),
            "nutrition": NutritionAgent()
        }

    async def route_request(self, request_type: str, data: Any) -> Dict[str, Any]:
        logger.info(f"Orchestrator received request: {request_type}")
        
        agent = self.agents.get(request_type)
        if not agent:
            return {"error": f"No agent found for request type: {request_type}"}
        
        # Async execution of the agent
        try:
            result = await agent.process(data)
            return {
                "success": True,
                "orchestrator_id": "health_watch_core_v1",
                "result": result
            }
        except Exception as e:
            logger.error(f"Error in agent execution: {e}")
            return {"success": False, "error": str(e)}

    async def broadcast(self, data: Any) -> Dict[str, Any]:
        """Send data to all agents for comprehensive analysis."""
        tasks = [agent.process(data) for agent in self.agents.values()]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        final_report = {}
        for agent_name, result in zip(self.agents.keys(), results):
            if isinstance(result, Exception):
                final_report[agent_name] = {"error": str(result)}
            else:
                final_report[agent_name] = result
                
        return {
            "type": "comprehensive_report",
            "results": final_report
        }

agent_orchestrator = AgentOrchestrator()
