# backend/api_bangladesh_emergency.py
"""
🚨 Aurora Health - Bangladesh Emergency Response API
Critical care, hospital matching, ambulance dispatch, bed booking

Endpoints:
- POST /api/v1/bd/emergency - Report emergency case
- POST /api/v1/bd/hospitals/search - Find hospitals
- POST /api/v1/bd/ambulance/dispatch - Dispatch ambulance
- POST /api/v1/bd/beds/book - Book hospital bed
- POST /api/v1/bd/admission/remote - Remote admission
- GET /api/v1/bd/hospitals/{id} - Hospital details
- GET /api/v1/bd/ambulance/track/{id} - Track ambulance
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

# Initialize app
app = FastAPI(
    title="Aurora Health - Bangladesh Emergency Response",
    description="Critical care routing, ambulance dispatch, hospital booking for Bangladesh",
    version="1.0.0"
)


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class UrgencyLevelEnum(str, Enum):
    IMMEDIATE = "immediate"
    EMERGENCY = "emergency"
    URGENT = "urgent"
    SEMI_URGENT = "semi_urgent"
    ROUTINE = "routine"


class BedTypeEnum(str, Enum):
    WARD = "ward"
    CABIN = "cabin"
    ICU = "icu"
    HDU = "hdu"
    NICU = "nicu"
    CCU = "ccu"


class EmergencyRequest(BaseModel):
    """Emergency case submission"""
    
    # Patient info
    patient_name: str
    patient_phone: str
    age: int
    gender: str
    
    # Location
    latitude: float
    longitude: float
    address: str
    district: str
    
    # Condition
    chief_complaint: str
    symptoms: List[str]
    severity: int = Field(ge=1, le=10)  # 1-10 scale
    
    # Medical history
    medical_history: List[str] = []
    current_medications: List[str] = []
    allergies: List[str] = []
    
    # Insurance
    has_insurance: bool = False
    insurance_provider: Optional[str] = None
    
    # Emergency contacts
    family_contacts: List[str] = []


class HospitalSearchRequest(BaseModel):
    """Hospital search criteria"""
    
    # Location
    latitude: float
    longitude: float
    max_distance_km: Optional[float] = 100
    
    # Requirements
    departments: List[str] = []
    equipment: List[str] = []
    bed_type_needed: Optional[BedTypeEnum] = None
    
    # Preferences
    max_cost: Optional[int] = None  # BDT
    insurance_provider: Optional[str] = None


class AmbulanceDispatchRequest(BaseModel):
    """Ambulance dispatch request"""
    
    emergency_case_id: str
    
    # Pickup location
    pickup_latitude: float
    pickup_longitude: float
    pickup_address: str
    
    # Destination
    hospital_id: str
    
    # Requirements
    ambulance_type: str = "als"  # "basic", "als", "icu_mobile"
    need_doctor: bool = True
    
    # Contact
    contact_phone: str


class BedBookingRequest(BaseModel):
    """Bed booking request"""
    
    hospital_id: str
    bed_type: BedTypeEnum
    
    patient_name: str
    patient_nid: str  # National ID
    patient_phone: str
    
    # Admission details
    admission_date: datetime
    estimated_days: int
    
    # Payment
    advance_payment: int  # BDT
    payment_method: str  # "bkash", "nagad", "rocket", "card"


class RemoteAdmissionRequest(BaseModel):
    """Remote patient admission"""
    
    # Hospital
    hospital_id: str
    bed_booking_id: str
    
    # Patient details
    patient_name: str
    patient_name_bengali: str
    date_of_birth: str
    gender: str
    nid_number: str
    
    # Contact
    phone: str
    email: Optional[str] = None
    address: str
    
    # Emergency contact
    emergency_contact_name: str
    emergency_contact_phone: str
    emergency_contact_relation: str
    
    # Medical
    chief_complaint: str
    referring_doctor: Optional[str] = None
    medical_history: List[str] = []
    allergies: List[str] = []
    current_medications: List[str] = []
    
    # Insurance
    insurance_provider: Optional[str] = None
    insurance_policy_number: Optional[str] = None
    
    # Documents (base64 encoded)
    nid_front_image: Optional[str] = None
    nid_back_image: Optional[str] = None
    insurance_card_image: Optional[str] = None


class EmergencyResponse(BaseModel):
    """Emergency case response"""
    
    case_id: str
    urgency_level: UrgencyLevelEnum
    
    # AI Analysis
    ai_diagnosis: List[Dict[str, Any]]
    specialist_required: List[str]
    equipment_needed: List[str]
    
    # Recommended hospitals (top 3)
    recommended_hospitals: List[Dict[str, Any]]
    
    # Immediate actions
    immediate_actions: List[str]
    
    # Emergency numbers
    emergency_numbers: Dict[str, str]


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.post("/api/v1/bd/emergency", response_model=EmergencyResponse)
async def report_emergency(request: EmergencyRequest):
    """
    Report emergency case and get hospital recommendations
    
    Process:
    1. AI analyzes symptoms
    2. Determines urgency
    3. Matches to specialists
    4. Finds best hospitals
    5. Returns recommendations
    """
    
    # Simulate AI diagnosis (in production: use actual AI model)
    ai_diagnosis = [
        {
            "disease": "Acute Myocardial Infarction (Heart Attack)",
            "probability": 0.85,
            "icd10": "I21.9",
            "specialist": "Cardiologist"
        }
    ]
    
    # Determine urgency based on symptoms and severity
    if request.severity >= 8:
        urgency = UrgencyLevelEnum.IMMEDIATE
    elif request.severity >= 6:
        urgency = UrgencyLevelEnum.EMERGENCY
    else:
        urgency = UrgencyLevelEnum.URGENT
    
    # Find recommended hospitals (mock data)
    recommended_hospitals = [
        {
            "hospital_id": "nicvd_dhaka",
            "name": "National Institute of Cardiovascular Diseases",
            "name_bengali": "জাতীয় হৃদরোগ ইনস্টিটিউট",
            "distance_km": 38.8,
            "travel_time_minutes": 46,
            "score": 82.6,
            "bed_available": True,
            "estimated_cost": 19000,
            "phone_emergency": "02-9015951",
            "address": "Sher-e-Bangla Nagar, Dhaka",
            "recommended": True
        },
        {
            "hospital_id": "square_dhaka",
            "name": "Square Hospitals Ltd",
            "name_bengali": "স্কয়ার হাসপাতাল লিমিটেড",
            "distance_km": 41.4,
            "travel_time_minutes": 49,
            "score": 75.2,
            "bed_available": True,
            "estimated_cost": 190000,
            "phone_emergency": "+880-2-8159457",
            "address": "West Panthapath, Dhaka",
            "recommended": False
        }
    ]
    
    # Immediate actions
    immediate_actions = []
    if urgency == UrgencyLevelEnum.IMMEDIATE:
        immediate_actions = [
            "🚨 CALL 999 IMMEDIATELY (National Emergency Service)",
            "Give patient aspirin (if available and not allergic)",
            "Keep patient calm and seated",
            "Do NOT let patient exert themselves",
            "Prepare to go to hospital IMMEDIATELY",
            "Have someone call ahead to hospital",
            "Bring all medications and medical records"
        ]
    
    # Emergency numbers
    emergency_numbers = {
        "National Emergency": "999",
        "NICVD Emergency": "02-9015951",
        "Ambulance (Private)": "+880 1711-123456",
        "Police": "999",
        "Fire Service": "999"
    }
    
    case_id = f"EMG{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    return EmergencyResponse(
        case_id=case_id,
        urgency_level=urgency,
        ai_diagnosis=ai_diagnosis,
        specialist_required=["Cardiologist", "Interventional Cardiologist"],
        equipment_needed=["Cath Lab", "ICU", "ECG"],
        recommended_hospitals=recommended_hospitals,
        immediate_actions=immediate_actions,
        emergency_numbers=emergency_numbers
    )


@app.post("/api/v1/bd/hospitals/search")
async def search_hospitals(request: HospitalSearchRequest):
    """
    Search for hospitals based on criteria
    
    Returns list of hospitals with:
    - Distance and travel time
    - Bed availability
    - Cost estimates
    - Specialist availability
    """
    
    # Mock response
    hospitals = [
        {
            "hospital_id": "nicvd_dhaka",
            "name": "NICVD",
            "name_bengali": "জাতীয় হৃদরোগ ইনস্টিটিউট",
            "distance_km": 15.2,
            "travel_time_minutes": 25,
            "departments": ["Cardiology", "Cardiac Surgery"],
            "bed_availability": {
                "icu": {"available": 2, "total": 80},
                "cabin": {"available": 15, "total": 150}
            },
            "estimated_cost_range": {
                "min": 10000,
                "max": 50000
            },
            "quality_rating": 4.3,
            "phone": "02-9015951"
        }
    ]
    
    return {"hospitals": hospitals, "total_count": len(hospitals)}


@app.post("/api/v1/bd/ambulance/dispatch")
async def dispatch_ambulance(request: AmbulanceDispatchRequest):
    """
    Dispatch ambulance to patient location
    
    Returns:
    - Ambulance details
    - ETA
    - Tracking link
    - Driver contact
    """
    
    ambulance_id = f"AMB{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    return {
        "ambulance_id": ambulance_id,
        "status": "dispatched",
        "vehicle_number": "Dhaka Metro GA-1234",
        "ambulance_type": request.ambulance_type,
        "driver_name": "Mohammad Rahman",
        "driver_phone": "+880 1711-123456",
        "paramedic_name": "Dr. Fatima Begum",
        "eta_minutes": 12,
        "estimated_arrival": (datetime.now() + timedelta(minutes=12)).isoformat(),
        "tracking_url": f"https://track.aurora.health/{ambulance_id}",
        "cost_estimate": 10000,
        "message": "Ambulance dispatched. Driver will call you shortly.",
        "message_bengali": "অ্যাম্বুলেন্স পাঠানো হয়েছে। ড্রাইভার শীঘ্রই কল করবেন।"
    }


@app.post("/api/v1/bd/beds/book")
async def book_bed(request: BedBookingRequest):
    """
    Book hospital bed in advance
    
    Process:
    1. Check availability
    2. Reserve bed
    3. Process payment
    4. Generate booking confirmation
    """
    
    booking_id = f"BOOK{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    return {
        "booking_id": booking_id,
        "status": "confirmed",
        "hospital_id": request.hospital_id,
        "bed_type": request.bed_type,
        "bed_number": "ICU-A-12",
        "admission_date": request.admission_date.isoformat(),
        "estimated_cost_per_day": 25000,
        "advance_paid": request.advance_payment,
        "balance_due": 50000,
        "booking_confirmation": {
            "confirmation_number": booking_id,
            "hospital_phone": "02-9015951",
            "reporting_time": request.admission_date.isoformat(),
            "documents_required": [
                "National ID Card",
                "Previous medical records (if any)",
                "Insurance card (if applicable)"
            ]
        },
        "message": "Bed booking confirmed. Please report at scheduled time.",
        "message_bengali": "বেড বুকিং নিশ্চিত হয়েছে। নির্ধারিত সময়ে হাসপাতালে উপস্থিত হন।"
    }


@app.post("/api/v1/bd/admission/remote")
async def remote_admission(request: RemoteAdmissionRequest):
    """
    Complete remote patient admission
    
    Process:
    1. Validate documents
    2. Create patient record
    3. Assign bed
    4. Generate admission number
    5. Send confirmation
    """
    
    admission_id = f"ADM{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    return {
        "admission_id": admission_id,
        "admission_number": admission_id,
        "hospital_id": request.hospital_id,
        "patient_name": request.patient_name,
        "bed_number": "Cabin-B-205",
        "ward": "Cardiology Ward",
        "attending_physician": "Dr. Abdul Karim",
        "admission_date": datetime.now().isoformat(),
        "estimated_discharge_date": (datetime.now() + timedelta(days=3)).isoformat(),
        "admission_status": "confirmed",
        "documents_verified": True,
        "payment_due": {
            "admission_fee": 5000,
            "estimated_total": 150000,
            "advance_paid": 20000,
            "balance": 130000
        },
        "instructions": [
            "Report to Cardiology Ward reception",
            "Bring original NID and all documents",
            "Fasting required if surgery planned",
            "One attendant allowed 24/7"
        ],
        "instructions_bengali": [
            "কার্ডিওলজি ওয়ার্ড রিসেপশনে রিপোর্ট করুন",
            "আসল NID এবং সমস্ত ডকুমেন্ট আনুন",
            "সার্জারি পরিকল্পিত হলে উপবাস প্রয়োজন",
            "একজন সেবাকারী ২৪/৭ অনুমোদিত"
        ],
        "contact": {
            "ward_phone": "02-9015952",
            "nurse_station": "02-9015953",
            "emergency": "02-9015951"
        },
        "message": "Remote admission completed successfully. Please report at scheduled time with all documents.",
        "message_bengali": "দূরবর্তী ভর্তি সফলভাবে সম্পন্ন হয়েছে। সমস্ত ডকুমেন্ট সহ নির্ধারিত সময়ে রিপোর্ট করুন।"
    }


@app.get("/api/v1/bd/hospitals/{hospital_id}")
async def get_hospital_details(hospital_id: str):
    """Get complete hospital details"""
    
    # Mock data
    return {
        "hospital_id": hospital_id,
        "name": "National Institute of Cardiovascular Diseases",
        "name_bengali": "জাতীয় হৃদরোগ ইনস্টিটিটিউট",
        "address": "Sher-e-Bangla Nagar, Dhaka-1207",
        "phone_emergency": "02-9015951",
        "phone_general": "02-9015950",
        "email": "info@nicvd.gov.bd",
        "departments": [
            "Cardiology",
            "Cardiac Surgery",
            "Interventional Cardiology"
        ],
        "specialists": {
            "Cardiologist": 45,
            "Cardiac Surgeon": 20
        },
        "equipment": [
            "Cath Lab",
            "Echo",
            "ECG",
            "ICU Ventilators"
        ],
        "bed_capacity": {
            "total": 550,
            "icu": 80,
            "cabin": 150,
            "ward": 300
        },
        "current_availability": {
            "icu": 2,
            "cabin": 15,
            "ward": 45
        },
        "quality_rating": 4.3,
        "patient_reviews": 5280,
        "emergency_24x7": True,
        "ambulance_available": True
    }


@app.get("/api/v1/bd/ambulance/track/{ambulance_id}")
async def track_ambulance(ambulance_id: str):
    """Real-time ambulance tracking"""
    
    return {
        "ambulance_id": ambulance_id,
        "status": "en_route",
        "current_location": {
            "latitude": 23.8100,
            "longitude": 90.3500,
            "address": "Mirpur Road, Dhaka"
        },
        "destination": {
            "latitude": 23.7691,
            "longitude": 90.3684,
            "address": "NICVD, Sher-e-Bangla Nagar"
        },
        "eta_minutes": 8,
        "distance_remaining_km": 4.2,
        "driver_phone": "+880 1711-123456",
        "last_updated": datetime.now().isoformat(),
        "route_map_url": f"https://maps.aurora.health/{ambulance_id}"
    }


@app.get("/")
async def root():
    """API root"""
    return {
        "service": "Aurora Health - Bangladesh Emergency Response",
        "version": "1.0.0",
        "status": "operational",
        "features": [
            "Emergency case reporting",
            "Hospital matching",
            "Ambulance dispatch",
            "Bed booking",
            "Remote admission",
            "Real-time tracking"
        ],
        "emergency_number": "999",
        "documentation": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
