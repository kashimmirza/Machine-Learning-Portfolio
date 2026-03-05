import google.generativeai as genai
import os
from PIL import Image
import io

# Configure Gemini
# Ensure GEMINI_API_KEY is set in environment variables
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')

async def analyze_food_image(image_bytes: bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes))
        
        prompt = """
        Analyze this image and identify all food items.
        For each item, provide:
        1. Name of the food
        2. Estimated weight in grams
        3. Estimated calories
        4. Estimated protein (g)
        5. Estimated carbs (g)
        6. Estimated fat (g)
        
        Return the result as a JSON list of objects.
        Example format:
        [
            {"name": "Apple", "weight": 150, "calories": 95, "protein": 0.5, "carbs": 25, "fat": 0.3},
            ...
        ]
        """
        
        response = model.generate_content([prompt, image])
        
        # In a real app, we'd want to ensure valid JSON parsing here.
        # For now, we'll return the text and handle parsing in the controller or improve the prompt to force JSON.
        return response.text
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return None
