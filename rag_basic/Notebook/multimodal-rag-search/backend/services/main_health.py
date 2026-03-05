# backend/main_health.py
"""
🏥 Aurora Health AI - Main Application
Medical-grade AI healthcare platform

FastAPI application with:
- AI Doctor consultations
- Medical image analysis
- Symptom checking
- Medication management
- Health monitoring
"""

from fastapi import FastAPI, HTTPException, File, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
import uvicorn

# Medical AI services
from services.ai_doctor_assistant import get_ai_doctor, ConsultationType, UrgencyLevel
from services.medical_vision_language_model import (
    get_medical_vlm, 
    ImagingModality,
    get_dermatology_ai
)
from services.openai_pinecone_service import get_openai_pinecone_service
from databases.medical_knowledge_base import get_medical_kb

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Aurora Health AI",
    description="Medical-grade AI healthcare platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class SymptomInput(BaseModel):
    """Patient symptom input"""
    name: str = Field(..., description="Symptom name")
    severity: int = Field(..., ge=1, le=10, description="Severity 1-10")
    duration_hours: int = Field(..., ge=0, description="How long in hours")
    location: Optional[str] = Field(None, description="Body location")
    description: Optional[str] = Field(None, description="Additional details")


class PatientInfo(BaseModel):
    """Patient demographic and medical information"""
    age: int = Field(..., ge=0, le=120)
    sex: str = Field(..., description="Male, Female, Other")
    medical_history: Dict[str, Any] = Field(default_factory=dict)
    current_medications: List[str] = Field(default_factory=list)
    allergies: List[str] = Field(default_factory=list)
    family_history: Dict[str, Any] = Field(default_factory=dict)


class ConsultationRequest(BaseModel):
    """Request for AI doctor consultation"""
    patient_id: str
    chief_complaint: str = Field(..., description="What brings you in?")
    symptoms: List[SymptomInput] = Field(default_factory=list)
    patient_info: PatientInfo
    additional_context: Optional[str] = None


class ConsultationResponse(BaseModel):
    """AI doctor consultation response"""
    consultation_id: str
    timestamp: datetime
    urgency: str
    urgency_emoji: str
    differential_diagnosis: List[Dict[str, Any]]
    recommended_actions: List[str]
    reasoning: str
    confidence: float
    follow_up: str
    specialist_referral: Optional[str]
    emergency_warning: Optional[str]


class MedicalImageRequest(BaseModel):
    """Request for medical image analysis"""
    patient_id: str
    modality: str = Field(..., description="xray, ct, mri, skin_photo, etc")
    clinical_indication: str
    patient_age: int
    patient_sex: str
    medical_history: Dict[str, Any] = Field(default_factory=dict)


class MedicalImageResponse(BaseModel):
    """Medical image analysis response"""
    report_id: str
    timestamp: datetime
    study_type: str
    findings: List[Dict[str, Any]]
    impression: str
    recommendations: List[str]
    urgency: str
    confidence: float
    follow_up: str


class MedicationCheckRequest(BaseModel):
    """Request for medication interaction check"""
    medications: List[str] = Field(..., min_items=1)
    patient_info: Optional[PatientInfo] = None


class MedicationCheckResponse(BaseModel):
    """Medication interaction check response"""
    safe: bool
    interactions: List[Dict[str, Any]]
    warnings: List[str]
    recommendations: List[str]


class SymptomCheckRequest(BaseModel):
    """Quick symptom checker request"""
    symptoms: List[str]
    age: int
    sex: str


class SymptomCheckResponse(BaseModel):
    """Quick symptom checker response"""
    possible_conditions: List[Dict[str, Any]]
    urgency: str
    recommended_action: str
    when_to_seek_care: str


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Aurora Health AI",
        "version": "1.0.0",
        "status": "operational",
        "message": "Medical-grade AI healthcare platform",
        "endpoints": {
            "docs": "/api/docs",
            "health": "/health",
            "consultation": "/api/v1/consultation",
            "medical-image": "/api/v1/medical-image/analyze",
            "symptom-check": "/api/v1/symptom-check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        medical_kb = get_medical_kb()
        
        # Test AI service
        openai_service = get_openai_pinecone_service()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "medical_kb": "operational",
                "openai": "operational",
                "ai_doctor": "operational"
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")


# ============================================================================
# AI DOCTOR CONSULTATION
# ============================================================================

@app.post("/api/v1/consultation", response_model=ConsultationResponse)
async def ai_doctor_consultation(request: ConsultationRequest):
    """
    AI Doctor Consultation Endpoint
    
    Provides medical consultation with:
    - Symptom analysis
    - Differential diagnosis
    - Urgency assessment
    - Treatment recommendations
    - Specialist referrals
    
    Example:
        POST /api/v1/consultation
        {
            "patient_id": "patient_123",
            "chief_complaint": "chest pain",
            "symptoms": [
                {
                    "name": "chest pain",
                    "severity": 8,
                    "duration_hours": 2,
                    "location": "center of chest"
                }
            ],
            "patient_info": {
                "age": 55,
                "sex": "male",
                "medical_history": {"hypertension": true},
                "current_medications": ["Lisinopril"]
            }
        }
    """
    try:
        logger.info(f"Starting consultation for patient {request.patient_id}")
        
        # Initialize services
        openai_service = get_openai_pinecone_service()
        medical_kb = get_medical_kb()
        ai_doctor = get_ai_doctor(openai_service, medical_kb)
        
        # Prepare patient data
        patient_data = {
            'age': request.patient_info.age,
            'sex': request.patient_info.sex,
            'medical_history': request.patient_info.medical_history,
            'medications': request.patient_info.current_medications,
            'allergies': request.patient_info.allergies,
            'family_history': request.patient_info.family_history,
            'demographics': {
                'age': request.patient_info.age,
                'sex': request.patient_info.sex
            }
        }
        
        # Conduct consultation
        consultation = await ai_doctor.conduct_consultation(
            patient_id=request.patient_id,
            chief_complaint=request.chief_complaint,
            patient_data=patient_data
        )
        
        # Determine urgency emoji
        urgency_emojis = {
            "call_911_now": "🚨",
            "go_to_er_now": "⚠️",
            "urgent_care_today": "⏰",
            "see_doctor_24_48hrs": "📅",
            "see_doctor_this_week": "📋",
            "monitor_at_home": "🏠",
            "routine_followup": "✓"
        }
        
        # Check for emergency
        emergency_warning = None
        if consultation.urgency in [UrgencyLevel.CALL_911, UrgencyLevel.ER_NOW]:
            emergency_warning = "⚠️ MEDICAL EMERGENCY - Seek immediate care"
        
        # Format response
        response = ConsultationResponse(
            consultation_id=consultation.consultation_id,
            timestamp=consultation.timestamp,
            urgency=consultation.urgency.value,
            urgency_emoji=urgency_emojis.get(consultation.urgency.value, "ℹ️"),
            differential_diagnosis=[
                {
                    "diagnosis": dx["diagnosis"],
                    "probability": round(dx["probability"] * 100, 1),
                    "description": f"{dx['diagnosis']} ({round(dx['probability']*100, 1)}% likely)"
                }
                for dx in consultation.differential_diagnosis
            ],
            recommended_actions=consultation.recommended_actions,
            reasoning=consultation.reasoning,
            confidence=round(consultation.confidence * 100, 1),
            follow_up=consultation.follow_up or "As needed",
            specialist_referral=consultation.specialist_referral,
            emergency_warning=emergency_warning
        )
        
        logger.info(f"Consultation complete: {consultation.urgency.value}")
        
        return response
        
    except Exception as e:
        logger.error(f"Consultation error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Consultation failed: {str(e)}"
        )


# ============================================================================
# MEDICAL IMAGE ANALYSIS
# ============================================================================

@app.post("/api/v1/medical-image/analyze", response_model=MedicalImageResponse)
async def analyze_medical_image(
    image: UploadFile = File(...),
    patient_id: str = "",
    modality: str = "xray",
    clinical_indication: str = "",
    patient_age: int = 50,
    patient_sex: str = "unknown"
):
    """
    Analyze Medical Image (X-ray, CT, MRI, etc.)
    
    Upload medical image for AI analysis:
    - Radiology (X-ray, CT, MRI)
    - Dermatology (skin photos)
    - Pathology (microscopy)
    - Retinal imaging
    
    Returns detailed radiology report with:
    - Findings
    - Impression
    - Recommendations
    - Urgency level
    
    Example:
        POST /api/v1/medical-image/analyze
        Files: image=chest_xray.jpg
        Form: modality=xray, clinical_indication="cough and fever"
    """
    try:
        # Read image data
        image_data = await image.read()
        
        logger.info(f"Analyzing {modality} image for patient {patient_id}")
        
        # Initialize services
        openai_service = get_openai_pinecone_service()
        med_vlm = get_medical_vlm(openai_service)
        
        # Determine imaging modality
        modality_map = {
            'xray': ImagingModality.XRAY,
            'x-ray': ImagingModality.XRAY,
            'ct': ImagingModality.CT,
            'ct_scan': ImagingModality.CT,
            'mri': ImagingModality.MRI,
            'ultrasound': ImagingModality.ULTRASOUND,
            'skin': ImagingModality.DERMATOLOGY,
            'skin_photo': ImagingModality.DERMATOLOGY,
            'dermatology': ImagingModality.DERMATOLOGY,
            'pathology': ImagingModality.PATHOLOGY,
            'retinal': ImagingModality.RETINAL
        }
        
        imaging_modality = modality_map.get(
            modality.lower(),
            ImagingModality.XRAY
        )
        
        # Prepare clinical context
        clinical_context = {
            'indication': clinical_indication or 'Not specified'
        }
        
        patient_history = {
            'age': patient_age,
            'sex': patient_sex
        }
        
        # Analyze image
        report = await med_vlm.analyze_medical_image(
            image_data=image_data,
            modality=imaging_modality,
            clinical_context=clinical_context,
            patient_history=patient_history
        )
        
        # Format findings
        formatted_findings = [
            {
                "finding": finding.finding,
                "location": finding.location,
                "severity": finding.severity,
                "confidence": round(finding.confidence * 100, 1),
                "urgency": finding.urgency.value
            }
            for finding in report.findings
        ]
        
        # Create response
        response = MedicalImageResponse(
            report_id=f"report_{datetime.now().timestamp()}",
            timestamp=datetime.now(),
            study_type=report.study_type,
            findings=formatted_findings,
            impression=report.impression,
            recommendations=report.recommendations,
            urgency=report.urgency.value,
            confidence=round(report.confidence * 100, 1),
            follow_up=report.follow_up or "As clinically indicated"
        )
        
        logger.info(f"Image analysis complete: {len(formatted_findings)} findings")
        
        return response
        
    except Exception as e:
        logger.error(f"Image analysis error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Image analysis failed: {str(e)}"
        )


# ============================================================================
# MEDICATION INTERACTION CHECK
# ============================================================================

@app.post("/api/v1/medication/check", response_model=MedicationCheckResponse)
async def check_medication_interactions(request: MedicationCheckRequest):
    """
    Check Medication Interactions
    
    Analyzes drug-drug interactions for safety
    
    Example:
        POST /api/v1/medication/check
        {
            "medications": ["Warfarin", "Aspirin", "Ibuprofen"],
            "patient_info": {
                "age": 65,
                "sex": "female"
            }
        }
    """
    try:
        logger.info(f"Checking interactions for {len(request.medications)} medications")
        
        # Get medical knowledge base
        medical_kb = get_medical_kb()
        
        # Check interactions
        interactions = medical_kb.check_drug_interactions(request.medications)
        
        # Determine if safe
        severe_interactions = [
            i for i in interactions 
            if i.get('severity') in ['severe', 'major']
        ]
        
        safe = len(severe_interactions) == 0
        
        # Generate warnings
        warnings = []
        if severe_interactions:
            warnings.append(
                f"⚠️ {len(severe_interactions)} serious interaction(s) detected"
            )
            for interaction in severe_interactions:
                warnings.append(
                    f"{interaction['drug1']} + {interaction['drug2']}: "
                    f"{interaction['description']}"
                )
        
        # Generate recommendations
        recommendations = []
        if not safe:
            recommendations.append("Consult your doctor or pharmacist immediately")
            recommendations.append("Do not start these medications together without medical supervision")
        else:
            if len(interactions) > 0:
                recommendations.append("Minor interactions detected - monitor for side effects")
            else:
                recommendations.append("No significant interactions detected")
        
        response = MedicationCheckResponse(
            safe=safe,
            interactions=interactions,
            warnings=warnings,
            recommendations=recommendations
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Medication check error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Medication check failed: {str(e)}"
        )


# ============================================================================
# QUICK SYMPTOM CHECKER
# ============================================================================

@app.post("/api/v1/symptom-check", response_model=SymptomCheckResponse)
async def quick_symptom_check(request: SymptomCheckRequest):
    """
    Quick Symptom Checker
    
    Fast symptom assessment for common conditions
    
    Example:
        POST /api/v1/symptom-check
        {
            "symptoms": ["fever", "cough", "fatigue"],
            "age": 35,
            "sex": "female"
        }
    """
    try:
        logger.info(f"Quick symptom check: {request.symptoms}")
        
        # Get medical knowledge base
        medical_kb = get_medical_kb()
        
        # Query possible diseases
        possible_diseases = medical_kb.query_diseases(request.symptoms)
        
        # Format conditions
        possible_conditions = [
            {
                "condition": disease['name'],
                "probability": "High" if disease.get('prevalence', 0) > 0.1 else "Moderate",
                "description": disease.get('description', '')
            }
            for disease in possible_diseases[:5]
        ]
        
        # Determine urgency based on symptoms
        urgent_symptoms = ['chest pain', 'difficulty breathing', 'severe headache']
        is_urgent = any(
            urgent in ' '.join(request.symptoms).lower() 
            for urgent in urgent_symptoms
        )
        
        urgency = "URGENT - Seek care today" if is_urgent else "Non-urgent"
        
        recommended_action = (
            "See doctor within 24 hours" if is_urgent 
            else "Monitor symptoms, see doctor if worsening"
        )
        
        when_to_seek_care = (
            "If symptoms worsen or new symptoms develop - "
            "especially difficulty breathing, chest pain, or severe pain"
        )
        
        response = SymptomCheckResponse(
            possible_conditions=possible_conditions,
            urgency=urgency,
            recommended_action=recommended_action,
            when_to_seek_care=when_to_seek_care
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Symptom check error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Symptom check failed: {str(e)}"
        )


# ============================================================================
# SKIN LESION ANALYSIS (Dermatology AI)
# ============================================================================

@app.post("/api/v1/skin-check")
async def analyze_skin_lesion(
    image: UploadFile = File(...),
    patient_age: int = 40,
    patient_sex: str = "unknown",
    lesion_history: str = ""
):
    """
    Skin Cancer Screening
    
    Upload photo of mole/lesion for melanoma detection
    
    Returns:
    - Malignancy risk (Low/Medium/High)
    - ABCDE criteria assessment
    - Recommendations
    - When to see dermatologist
    """
    try:
        # Read image
        image_data = await image.read()
        
        # Initialize dermatology AI
        openai_service = get_openai_pinecone_service()
        derm_ai = get_dermatology_ai(openai_service)
        
        # Patient info
        patient_info = {
            'age': patient_age,
            'sex': patient_sex,
            'history': lesion_history
        }
        
        # Analyze skin lesion
        analysis = await derm_ai.analyze_skin_lesion(
            image_data=image_data,
            patient_info=patient_info
        )
        
        # Determine risk level
        risk = analysis['malignancy_risk']
        if risk > 0.5:
            risk_level = "HIGH"
            urgency = "See dermatologist within 1 week"
        elif risk > 0.2:
            risk_level = "MEDIUM"
            urgency = "See dermatologist within 2-4 weeks"
        else:
            risk_level = "LOW"
            urgency = "Monitor and photograph monthly"
        
        return {
            "risk_level": risk_level,
            "malignancy_probability": round(risk * 100, 1),
            "abcde_assessment": analysis['abcde_score'],
            "urgency": urgency,
            "recommendations": analysis['recommendations'],
            "warning": (
                "⚠️ This is a screening tool, not a diagnosis. "
                "Always see a dermatologist for concerning lesions."
            )
        }
        
    except Exception as e:
        logger.error(f"Skin analysis error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Skin analysis failed: {str(e)}"
        )


# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "main_health:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
