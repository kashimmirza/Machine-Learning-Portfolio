import base64
import cv2
import numpy as np
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from app.core.config import settings

class AnalysisService:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            api_key=settings.OPENAI_API_KEY,
            temperature=0.2,
            max_tokens=1000
        )

    async def analyze_medical_image(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Analyzes a medical image using GPT-4o for diagnosis and OpenCV for visual saliency.
        """
        # 1. Generate Visual Explanations (Saliency Map)
        processed_image_b64 = self._generate_saliency_map(image_bytes)
        
        # 2. Generate Textual Diagnosis
        image_b64 = base64.b64encode(image_bytes).decode('utf-8')
        diagnosis_report = await self._generate_diagnosis(image_b64)

        return {
            "report": diagnosis_report,
            "processed_image": processed_image_b64 
        }

    def _generate_saliency_map(self, image_bytes: bytes) -> str:
        """
        Uses OpenCV to create a heatmap/saliency map of the image.
        In a real scenario, this would use a segmentation model. 
        Here we use high-contrast edge/contour detection as a proxy for "Area of Interest".
        """
        # Decode image
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to enhance details
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # Apply Gaussian Blur to reduce noise
        blurred = cv2.GaussianBlur(enhanced, (5, 5), 0)
        
        # Canny Edge Detection to find structure
        edges = cv2.Canny(blurred, 50, 150)
        
        # Dilate edges to make them more visible suitable for a mask
        kernel = np.ones((3,3), np.uint8)
        dilated = cv2.dilate(edges, kernel, iterations=2)
        
        # Create a heatmap overlay (Red for edges)
        heatmap = np.zeros_like(img)
        heatmap[dilated > 0] = [0, 0, 255] # Red color for "damage/interest"
        
        # Blend original with heatmap
        blended = cv2.addWeighted(img, 0.7, heatmap, 0.3, 0)
        
        # Encode back to base64
        _, buffer = cv2.imencode('.jpg', blended)
        return base64.b64encode(buffer).decode('utf-8')

    async def _generate_diagnosis(self, image_b64: str) -> str:
        """
        Sends the image to GPT-4o for a professional medical report.
        """
        messages = [
            SystemMessage(content="""You are an expert Radiologist with 20 years of experience. 
            Analyze the provided medical image (CT Scan, X-Ray, or MRI).
            
            Provide a structured report using the following format:
            
            ## **Medical Analysis Report**
            **Modality:** [CT / X-Ray / MRI]
            **Region:** [Body Part]
            
            ### **Findings**
            - [List key observations, anomalies, or normal structures]
            
            ### **Potential Abnormality**
            - [Identify any fractures, tumors, lesions, or "None"]
            
            ### **Recommendation**
            - [Clinical advice or further tests]
            
            **Dislaimer:** This is an AI-generated analysis and should be verified by a human professional."""),
            HumanMessage(content=[
                {"type": "text", "text": "Please analyze this medical image."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
            ])
        ]
        
        response = await self.llm.ainvoke(messages)
        return response.content

analysis_service = AnalysisService()
