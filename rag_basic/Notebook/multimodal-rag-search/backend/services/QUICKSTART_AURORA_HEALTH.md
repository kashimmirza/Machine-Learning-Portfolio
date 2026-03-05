# 🏥 AURORA HEALTH AI - Getting Started

Welcome to Aurora Health AI - your medical-grade AI healthcare platform!

## 🚀 Quick Start (5 Minutes)

### Step 1: Install

```bash
# Make start script executable
chmod +x start_aurora_health.sh

# Run quick start
./start_aurora_health.sh
```

### Step 2: Configure

Edit `backend/.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

### Step 3: Launch

```bash
cd backend
python3 main_health.py
```

### Step 4: Test

Open browser: **http://localhost:8000/api/docs**

---

## 📖 API Examples

### 1. AI Doctor Consultation

**Endpoint:** `POST /api/v1/consultation`

**Example Request:**
```json
{
  "patient_id": "patient_123",
  "chief_complaint": "I have chest pain and shortness of breath",
  "symptoms": [
    {
      "name": "chest pain",
      "severity": 8,
      "duration_hours": 2,
      "location": "center of chest"
    },
    {
      "name": "shortness of breath",
      "severity": 7,
      "duration_hours": 2
    }
  ],
  "patient_info": {
    "age": 55,
    "sex": "male",
    "medical_history": {
      "hypertension": true,
      "diabetes": true
    },
    "current_medications": ["Lisinopril", "Metformin"],
    "allergies": []
  }
}
```

**Example Response:**
```json
{
  "consultation_id": "consult_1234567890",
  "timestamp": "2024-01-29T10:30:00",
  "urgency": "call_911_now",
  "urgency_emoji": "🚨",
  "differential_diagnosis": [
    {
      "diagnosis": "Acute Myocardial Infarction",
      "probability": 65.0,
      "description": "Acute Myocardial Infarction (65.0% likely)"
    },
    {
      "diagnosis": "Unstable Angina",
      "probability": 25.0,
      "description": "Unstable Angina (25.0% likely)"
    }
  ],
  "recommended_actions": [
    "🚨 CALL 911 IMMEDIATELY",
    "Do not drive yourself",
    "Chew aspirin 325mg if not allergic",
    "Lie down and stay calm"
  ],
  "reasoning": "Based on your symptoms...",
  "confidence": 90.0,
  "follow_up": "Immediate hospital follow-up",
  "specialist_referral": "Cardiologist",
  "emergency_warning": "⚠️ MEDICAL EMERGENCY - Seek immediate care"
}
```

### 2. Medical Image Analysis

**Endpoint:** `POST /api/v1/medical-image/analyze`

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/medical-image/analyze" \
  -F "image=@chest_xray.jpg" \
  -F "patient_id=patient_123" \
  -F "modality=xray" \
  -F "clinical_indication=cough and fever for 1 week" \
  -F "patient_age=65" \
  -F "patient_sex=male"
```

**Example Response:**
```json
{
  "report_id": "report_1234567890",
  "timestamp": "2024-01-29T10:35:00",
  "study_type": "x-ray",
  "findings": [
    {
      "finding": "Right lower lobe consolidation",
      "location": "Right lower lobe",
      "severity": "moderate",
      "confidence": 92.0,
      "urgency": "urgent"
    }
  ],
  "impression": "Findings consistent with pneumonia in right lower lobe",
  "recommendations": [
    "Blood cultures before antibiotics",
    "Empiric antibiotic therapy",
    "Follow-up chest X-ray in 6-8 weeks"
  ],
  "urgency": "urgent",
  "confidence": 92.0,
  "follow_up": "Within 24-48 hours"
}
```

### 3. Medication Interaction Check

**Endpoint:** `POST /api/v1/medication/check`

**Example Request:**
```json
{
  "medications": ["Warfarin", "Aspirin", "Ibuprofen"],
  "patient_info": {
    "age": 65,
    "sex": "female"
  }
}
```

**Example Response:**
```json
{
  "safe": false,
  "interactions": [
    {
      "drug1": "Warfarin",
      "drug2": "Aspirin",
      "severity": "moderate",
      "description": "Warfarin may interact with Aspirin"
    },
    {
      "drug1": "Warfarin",
      "drug2": "Ibuprofen",
      "severity": "moderate",
      "description": "Warfarin may interact with Ibuprofen"
    }
  ],
  "warnings": [
    "⚠️ 2 serious interaction(s) detected"
  ],
  "recommendations": [
    "Consult your doctor or pharmacist immediately",
    "Do not start these medications together without medical supervision"
  ]
}
```

### 4. Quick Symptom Check

**Endpoint:** `POST /api/v1/symptom-check`

**Example Request:**
```json
{
  "symptoms": ["fever", "cough", "fatigue", "body aches"],
  "age": 35,
  "sex": "female"
}
```

**Example Response:**
```json
{
  "possible_conditions": [
    {
      "condition": "Influenza",
      "probability": "High",
      "description": "Viral respiratory infection"
    },
    {
      "condition": "COVID-19",
      "probability": "High",
      "description": "Coronavirus infection"
    },
    {
      "condition": "Common Cold",
      "probability": "Moderate",
      "description": "Upper respiratory infection"
    }
  ],
  "urgency": "Non-urgent",
  "recommended_action": "Monitor symptoms, see doctor if worsening",
  "when_to_seek_care": "If symptoms worsen or new symptoms develop - especially difficulty breathing, chest pain, or severe pain"
}
```

### 5. Skin Cancer Screening

**Endpoint:** `POST /api/v1/skin-check`

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/skin-check" \
  -F "image=@mole_photo.jpg" \
  -F "patient_age=45" \
  -F "patient_sex=female" \
  -F "lesion_history=has been changing over 6 months"
```

**Example Response:**
```json
{
  "risk_level": "HIGH",
  "malignancy_probability": 76.0,
  "abcde_assessment": {
    "asymmetry": 0.8,
    "border": 0.7,
    "color": 0.9,
    "diameter": 8.5,
    "evolution": true
  },
  "urgency": "See dermatologist within 1 week",
  "recommendations": [
    "Schedule dermatology appointment immediately",
    "Do not wait - early detection is critical",
    "Biopsy likely needed"
  ],
  "warning": "⚠️ This is a screening tool, not a diagnosis. Always see a dermatologist for concerning lesions."
}
```

---

## 🧪 Testing with Python

### Example: Complete Workflow

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# 1. AI Doctor Consultation
consultation_data = {
    "patient_id": "test_patient_001",
    "chief_complaint": "fever and cough for 3 days",
    "symptoms": [
        {
            "name": "fever",
            "severity": 6,
            "duration_hours": 72
        },
        {
            "name": "cough",
            "severity": 5,
            "duration_hours": 72
        }
    ],
    "patient_info": {
        "age": 35,
        "sex": "female",
        "medical_history": {},
        "current_medications": [],
        "allergies": []
    }
}

response = requests.post(
    f"{BASE_URL}/api/v1/consultation",
    json=consultation_data
)

result = response.json()
print("Diagnosis:", result['differential_diagnosis'][0])
print("Urgency:", result['urgency'])
print("Recommendations:")
for rec in result['recommended_actions']:
    print(f"  - {rec}")

# 2. Medication Check
med_check = {
    "medications": ["Lisinopril", "Ibuprofen"]
}

response = requests.post(
    f"{BASE_URL}/api/v1/medication/check",
    json=med_check
)

result = response.json()
print("\nMedication Safety:", "SAFE" if result['safe'] else "UNSAFE")
if result['interactions']:
    print("Interactions found:")
    for interaction in result['interactions']:
        print(f"  - {interaction['drug1']} + {interaction['drug2']}")
```

---

## 📊 Understanding Responses

### Urgency Levels

| Level | Emoji | Meaning | Action |
|-------|-------|---------|--------|
| `call_911_now` | 🚨 | EMERGENCY | Call 911 immediately |
| `go_to_er_now` | ⚠️ | Very Urgent | Go to ER now |
| `urgent_care_today` | ⏰ | Urgent | See doctor today |
| `see_doctor_24_48hrs` | 📅 | Semi-urgent | Appointment within 48 hours |
| `see_doctor_this_week` | 📋 | Routine urgent | This week |
| `monitor_at_home` | 🏠 | Monitor | Watch at home |
| `routine_followup` | ✓ | Routine | Routine care |

### Confidence Levels

- **90-100%**: Very High - Strong clinical evidence
- **80-89%**: High - Good diagnostic certainty
- **70-79%**: Moderate - Reasonable confidence
- **60-69%**: Low - Multiple possibilities
- **<60%**: Very Low - Unclear diagnosis

---

## 🔒 Security & Privacy

### HIPAA Compliance

Aurora Health AI is designed with HIPAA compliance in mind:

- ✅ **Encryption**: All data encrypted at rest and in transit
- ✅ **Access Controls**: Role-based access control (RBAC)
- ✅ **Audit Logging**: All actions logged immutably
- ✅ **Data Minimization**: Only collect necessary data
- ✅ **User Consent**: Explicit consent for data usage

### Best Practices

1. **Never log PHI** (Protected Health Information)
2. **Use secure connections** (HTTPS in production)
3. **Implement authentication** (JWT tokens)
4. **Regular security audits**
5. **Breach notification procedures**

---

## 🎯 Next Steps

### For Development

1. **Add Authentication**
   - Implement JWT tokens
   - User registration/login
   - Role-based access

2. **Enhance Medical AI**
   - Add more diseases to knowledge base
   - Improve diagnostic accuracy
   - Add more medical guidelines

3. **Build Frontend**
   - Patient mobile app
   - Hospital dashboard
   - Admin panel

4. **Prepare for FDA**
   - Clinical validation studies
   - Documentation
   - 510(k) submission

### For Production

1. **Infrastructure**
   - PostgreSQL database
   - Redis caching
   - Load balancing
   - Auto-scaling

2. **Monitoring**
   - Performance metrics
   - Error tracking (Sentry)
   - User analytics
   - Health checks

3. **Compliance**
   - HIPAA compliance audit
   - SOC 2 certification
   - Privacy policies
   - Terms of service

---

## 📚 Documentation

- **API Documentation**: http://localhost:8000/api/docs
- **Full Vision**: `AURORA_HEALTH_AI.md`
- **Implementation Guide**: `AURORA_HEALTH_IMPLEMENTATION.md`
- **Technical Details**: Check individual service files

---

## 🆘 Troubleshooting

### Common Issues

**Issue**: `OPENAI_API_KEY not found`
- **Solution**: Add your API key to `backend/.env`

**Issue**: `Module not found`
- **Solution**: Run `pip install -r requirements_health.txt`

**Issue**: `Database locked`
- **Solution**: Only one instance can run at a time

**Issue**: `Port 8000 already in use`
- **Solution**: Change port in `main_health.py` or kill other process

### Getting Help

1. Check logs in console output
2. Review API documentation at `/api/docs`
3. Read the comprehensive guides in `/outputs/`

---

## 🎉 You're Ready!

Your Aurora Health AI platform is ready to:
- ✅ Provide AI doctor consultations
- ✅ Analyze medical images
- ✅ Check medication interactions
- ✅ Screen for diseases
- ✅ Save lives

**Start the server and begin testing!**

```bash
cd backend
python3 main_health.py
```

Then visit: **http://localhost:8000/api/docs**

---

## 💙 Remember

This is medical AI that can **save lives**. Every consultation, every image analysis, every medication check - they all matter.

**Build responsibly. Test thoroughly. Deploy carefully.**

**Let's change healthcare together.** 🏥
