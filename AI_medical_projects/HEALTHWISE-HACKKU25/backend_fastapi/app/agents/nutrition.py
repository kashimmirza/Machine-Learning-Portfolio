from typing import Any, Dict
from app.agents.base import BaseAgent

class NutritionAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="NutritionAgent")

    async def process(self, input_data: Any) -> Dict[str, Any]:
        calories = input_data.get('calories', 0)
        meal_type = input_data.get('meal_type', 'Snack')
        
        advice = "Good balance."
        if calories > 800:
            advice = "High caloric intake for a single meal. Suggest light activity."
            
        return {
            "agent": self.name,
            "analysis": f"Meal: {meal_type} ({calories} kcal).",
            "recommendation": advice
        }
