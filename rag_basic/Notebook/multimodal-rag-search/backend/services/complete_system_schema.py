# backend/databases/complete_system_schema.py
"""
🏥 Aurora Health - Complete Database Schema
Enterprise-grade healthcare database design

Databases:
- PostgreSQL (main operational database)
- MongoDB (document storage - imaging reports, notes)
- Redis (caching, real-time data)
- Elasticsearch (full-text search)
- TimescaleDB (time-series - vital signs, monitoring)
"""

from sqlalchemy import (
    create_engine, Column, String, Integer, Float, Boolean,
    DateTime, Date, JSON, ForeignKey, Text, Enum as SQLEnum,
    Index, UniqueConstraint, CheckConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import enum

Base = declarative_base()


# ============================================================================
# ENUMS
# ============================================================================

class UserRoleEnum(enum.Enum):
    PATIENT = "patient"
    DOCTOR = "doctor"
    NURSE = "nurse"
    ADMIN = "admin"
    PHARMACIST = "pharmacist"
    PAYER = "payer"


class GenderEnum(enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"


class AppointmentStatusEnum(enum.Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class ClaimStatusEnum(enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    DENIED = "denied"
    APPEALED = "appealed"
    PAID = "paid"


# ============================================================================
# CORE TABLES
# ============================================================================

class User(Base):
    """Core user table - all system users"""
    __tablename__ = 'users'
    
    user_id = Column(String(36), primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20))
    role = Column(SQLEnum(UserRoleEnum), nullable=False, index=True)
    
    active = Column(Boolean, default=True, index=True)
    email_verified = Column(Boolean, default=False)
    phone_verified = Column(Boolean, default=False)
    
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patient_profile = relationship("Patient", back_populates="user", uselist=False)
    provider_profile = relationship("Provider", back_populates="user", uselist=False)
    
    __table_args__ = (
        Index('idx_user_email', 'email'),
        Index('idx_user_role', 'role'),
    )


class Patient(Base):
    """Patient profile"""
    __tablename__ = 'patients'
    
    patient_id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey('users.user_id'), unique=True, nullable=False)
    
    # Demographics
    date_of_birth = Column(Date, nullable=False)
    gender = Column(SQLEnum(GenderEnum), nullable=False)
    race = Column(String(50))
    ethnicity = Column(String(50))
    preferred_language = Column(String(10), default='en')
    
    # Contact
    address_street = Column(String(255))
    address_city = Column(String(100))
    address_state = Column(String(2))
    address_zip = Column(String(10))
    address_country = Column(String(2), default='US')
    
    emergency_contact_name = Column(String(255))
    emergency_contact_phone = Column(String(20))
    emergency_contact_relationship = Column(String(50))
    
    # Medical
    blood_type = Column(String(5))
    allergies = Column(JSON)  # List of allergies
    chronic_conditions = Column(JSON)  # List of conditions
    
    # Preferences
    primary_care_physician_id = Column(String(36), ForeignKey('providers.provider_id'))
    preferred_pharmacy_id = Column(String(36))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="patient_profile")
    appointments = relationship("Appointment", back_populates="patient")
    prescriptions = relationship("Prescription", back_populates="patient")
    vital_signs = relationship("VitalSigns", back_populates="patient")
    
    __table_args__ = (
        Index('idx_patient_user', 'user_id'),
        Index('idx_patient_dob', 'date_of_birth'),
    )


class Provider(Base):
    """Healthcare provider (doctor, nurse, etc.)"""
    __tablename__ = 'providers'
    
    provider_id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey('users.user_id'), unique=True, nullable=False)
    
    # Credentials
    npi = Column(String(10), unique=True, index=True)  # National Provider Identifier
    license_number = Column(String(50))
    license_state = Column(String(2))
    dea_number = Column(String(20))  # For prescribing controlled substances
    
    # Professional
    specialty = Column(String(100), index=True)
    sub_specialty = Column(String(100))
    board_certified = Column(Boolean, default=False)
    
    # Practice
    practice_name = Column(String(255))
    office_address = Column(String(500))
    office_phone = Column(String(20))
    
    # Insurance
    accepting_new_patients = Column(Boolean, default=True)
    insurance_networks = Column(JSON)  # List of accepted insurance networks
    
    # Metrics
    average_rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="provider_profile")
    appointments = relationship("Appointment", back_populates="provider")
    prescriptions = relationship("Prescription", foreign_keys="[Prescription.prescriber_id]")
    
    __table_args__ = (
        Index('idx_provider_npi', 'npi'),
        Index('idx_provider_specialty', 'specialty'),
    )


# ============================================================================
# APPOINTMENT & SCHEDULING
# ============================================================================

class Appointment(Base):
    """Patient appointments"""
    __tablename__ = 'appointments'
    
    appointment_id = Column(String(36), primary_key=True)
    patient_id = Column(String(36), ForeignKey('patients.patient_id'), nullable=False, index=True)
    provider_id = Column(String(36), ForeignKey('providers.provider_id'), nullable=False, index=True)
    
    # Schedule
    scheduled_start = Column(DateTime, nullable=False, index=True)
    scheduled_end = Column(DateTime, nullable=False)
    
    # Details
    appointment_type = Column(String(50), nullable=False)  # office_visit, telehealth, etc.
    reason = Column(Text, nullable=False)
    notes = Column(Text)
    
    # Location
    location_id = Column(String(36))
    room_number = Column(String(20))
    
    # Status
    status = Column(SQLEnum(AppointmentStatusEnum), nullable=False, default=AppointmentStatusEnum.SCHEDULED, index=True)
    
    # Check-in/out
    check_in_time = Column(DateTime)
    check_out_time = Column(DateTime)
    actual_start = Column(DateTime)
    actual_end = Column(DateTime)
    
    # Notifications
    confirmation_sent = Column(Boolean, default=False)
    reminder_sent = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    provider = relationship("Provider", back_populates="appointments")
    
    __table_args__ = (
        Index('idx_appt_patient_date', 'patient_id', 'scheduled_start'),
        Index('idx_appt_provider_date', 'provider_id', 'scheduled_start'),
        Index('idx_appt_status', 'status'),
    )


# ============================================================================
# CLINICAL DOCUMENTATION
# ============================================================================

class Encounter(Base):
    """Clinical encounter"""
    __tablename__ = 'encounters'
    
    encounter_id = Column(String(36), primary_key=True)
    patient_id = Column(String(36), ForeignKey('patients.patient_id'), nullable=False, index=True)
    provider_id = Column(String(36), ForeignKey('providers.provider_id'), nullable=False, index=True)
    
    appointment_id = Column(String(36), ForeignKey('appointments.appointment_id'))
    
    encounter_date = Column(DateTime, nullable=False, index=True)
    encounter_type = Column(String(50), nullable=False)
    
    # Clinical
    chief_complaint = Column(Text, nullable=False)
    
    # Codes
    icd10_codes = Column(JSON)  # Diagnosis codes
    cpt_codes = Column(JSON)  # Procedure codes
    
    # Status
    status = Column(String(20), default='active')
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    notes = relationship("ClinicalNote", back_populates="encounter")
    
    __table_args__ = (
        Index('idx_encounter_patient_date', 'patient_id', 'encounter_date'),
    )


class ClinicalNote(Base):
    """Clinical documentation (SOAP notes, etc.)"""
    __tablename__ = 'clinical_notes'
    
    note_id = Column(String(36), primary_key=True)
    encounter_id = Column(String(36), ForeignKey('encounters.encounter_id'), nullable=False, index=True)
    
    # SOAP
    subjective = Column(Text)
    objective = Column(Text)
    assessment = Column(Text)
    plan = Column(Text)
    
    note_type = Column(String(50), nullable=False)
    
    # Signature
    signed_at = Column(DateTime)
    signed_by = Column(String(36), ForeignKey('providers.provider_id'))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    encounter = relationship("Encounter", back_populates="notes")


# ============================================================================
# MEDICATIONS
# ============================================================================

class Medication(Base):
    """Medication formulary"""
    __tablename__ = 'medications'
    
    medication_id = Column(String(36), primary_key=True)
    
    name = Column(String(255), nullable=False, index=True)
    generic_name = Column(String(255), nullable=False, index=True)
    brand_names = Column(JSON)
    
    drug_class = Column(String(100), index=True)
    
    # Codes
    rxnorm_code = Column(String(20), unique=True, index=True)
    ndc_code = Column(String(20))
    
    # Clinical info (stored as JSON for flexibility)
    indications = Column(JSON)
    contraindications = Column(JSON)
    side_effects = Column(JSON)
    interactions = Column(JSON)
    
    # Regulatory
    fda_approved = Column(Boolean, default=True)
    controlled_substance_schedule = Column(String(5))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_med_name', 'name'),
        Index('idx_med_generic', 'generic_name'),
    )


class Prescription(Base):
    """Electronic prescriptions"""
    __tablename__ = 'prescriptions'
    
    prescription_id = Column(String(36), primary_key=True)
    patient_id = Column(String(36), ForeignKey('patients.patient_id'), nullable=False, index=True)
    prescriber_id = Column(String(36), ForeignKey('providers.provider_id'), nullable=False, index=True)
    
    medication_id = Column(String(36), ForeignKey('medications.medication_id'), nullable=False)
    medication_name = Column(String(255), nullable=False)
    
    # Dosing
    directions = Column(Text, nullable=False)
    quantity = Column(Float, nullable=False)
    days_supply = Column(Integer, nullable=False)
    refills = Column(Integer, nullable=False, default=0)
    
    # Dispensing
    pharmacy_id = Column(String(36))
    dispense_as_written = Column(Boolean, default=False)
    
    # Status
    status = Column(String(20), default='active', index=True)
    prescribed_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    filled_date = Column(DateTime)
    
    # E-prescribing
    erx_message_id = Column(String(100))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient", back_populates="prescriptions")
    
    __table_args__ = (
        Index('idx_rx_patient_status', 'patient_id', 'status'),
    )


# ============================================================================
# LAB & IMAGING
# ============================================================================

class LabOrder(Base):
    """Laboratory orders"""
    __tablename__ = 'lab_orders'
    
    order_id = Column(String(36), primary_key=True)
    patient_id = Column(String(36), ForeignKey('patients.patient_id'), nullable=False, index=True)
    ordering_provider_id = Column(String(36), ForeignKey('providers.provider_id'), nullable=False)
    
    # Test
    test_code = Column(String(20), nullable=False)  # LOINC code
    test_name = Column(String(255), nullable=False)
    
    clinical_indication = Column(Text)
    priority = Column(String(20), default='routine')
    
    # Dates
    order_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    collection_date = Column(DateTime)
    result_date = Column(DateTime)
    
    status = Column(String(20), default='ordered', index=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    results = relationship("LabResult", back_populates="order")
    
    __table_args__ = (
        Index('idx_lab_patient_date', 'patient_id', 'order_date'),
    )


class LabResult(Base):
    """Laboratory results"""
    __tablename__ = 'lab_results'
    
    result_id = Column(String(36), primary_key=True)
    order_id = Column(String(36), ForeignKey('lab_orders.order_id'), nullable=False, index=True)
    
    test_code = Column(String(20), nullable=False)
    test_name = Column(String(255), nullable=False)
    
    value = Column(String(100), nullable=False)
    unit = Column(String(50))
    reference_range = Column(String(100))
    abnormal_flag = Column(String(5))  # H, L, A, etc.
    
    result_date = Column(DateTime, nullable=False)
    
    # Review
    reviewed = Column(Boolean, default=False)
    reviewed_by = Column(String(36), ForeignKey('providers.provider_id'))
    reviewed_date = Column(DateTime)
    
    comments = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    order = relationship("LabOrder", back_populates="results")
    
    __table_args__ = (
        Index('idx_result_order', 'order_id'),
    )


# ============================================================================
# VITAL SIGNS (Time-series data - use TimescaleDB)
# ============================================================================

class VitalSigns(Base):
    """Patient vital signs"""
    __tablename__ = 'vital_signs'
    
    vital_id = Column(String(36), primary_key=True)
    patient_id = Column(String(36), ForeignKey('patients.patient_id'), nullable=False, index=True)
    
    timestamp = Column(DateTime, nullable=False, index=True)
    
    # Vitals
    temperature = Column(Float)  # Celsius
    blood_pressure_systolic = Column(Integer)
    blood_pressure_diastolic = Column(Integer)
    heart_rate = Column(Integer)
    respiratory_rate = Column(Integer)
    oxygen_saturation = Column(Integer)
    
    weight = Column(Float)  # kg
    height = Column(Float)  # cm
    bmi = Column(Float)
    
    # Source
    recorded_by = Column(String(36))  # user_id or device_id
    source = Column(String(50))  # manual, wearable, monitor
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    patient = relationship("Patient", back_populates="vital_signs")
    
    __table_args__ = (
        Index('idx_vitals_patient_time', 'patient_id', 'timestamp'),
    )


# ============================================================================
# HOSPITAL MANAGEMENT
# ============================================================================

class Admission(Base):
    """Hospital admissions"""
    __tablename__ = 'admissions'
    
    admission_id = Column(String(36), primary_key=True)
    patient_id = Column(String(36), ForeignKey('patients.patient_id'), nullable=False, index=True)
    
    admission_date = Column(DateTime, nullable=False, index=True)
    discharge_date = Column(DateTime)
    
    admission_type = Column(String(50))  # elective, emergency, etc.
    admission_source = Column(String(50))  # ED, clinic, transfer
    
    # Provider
    admitting_provider_id = Column(String(36), ForeignKey('providers.provider_id'))
    attending_physician_id = Column(String(36), ForeignKey('providers.provider_id'))
    
    # Location
    bed_id = Column(String(36))
    room_number = Column(String(20))
    unit = Column(String(50))
    
    # Clinical
    primary_diagnosis = Column(String(10))  # ICD-10
    diagnosis_description = Column(String(255))
    
    # Status
    status = Column(String(20), default='active', index=True)
    discharge_disposition = Column(String(50))
    
    # Metrics
    length_of_stay_days = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_admission_patient_date', 'patient_id', 'admission_date'),
        Index('idx_admission_status', 'status'),
    )


# ============================================================================
# INSURANCE & BILLING
# ============================================================================

class InsurancePlan(Base):
    """Insurance plans/payers"""
    __tablename__ = 'insurance_plans'
    
    plan_id = Column(String(36), primary_key=True)
    
    payer_name = Column(String(255), nullable=False, index=True)
    plan_name = Column(String(255), nullable=False)
    plan_type = Column(String(50))  # HMO, PPO, EPO, etc.
    
    # Identifiers
    payer_id = Column(String(20), unique=True)  # Clearinghouse payer ID
    
    # Contact
    phone = Column(String(20))
    website = Column(String(255))
    claims_address = Column(Text)
    
    active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class PatientInsurance(Base):
    """Patient insurance coverage"""
    __tablename__ = 'patient_insurance'
    
    patient_insurance_id = Column(String(36), primary_key=True)
    patient_id = Column(String(36), ForeignKey('patients.patient_id'), nullable=False, index=True)
    plan_id = Column(String(36), ForeignKey('insurance_plans.plan_id'), nullable=False)
    
    # Coverage
    coverage_type = Column(String(20))  # primary, secondary
    member_id = Column(String(50), nullable=False)
    group_number = Column(String(50))
    
    # Subscriber (if patient is dependent)
    subscriber_name = Column(String(255))
    subscriber_relationship = Column(String(50))
    subscriber_dob = Column(Date)
    
    # Dates
    effective_date = Column(Date, nullable=False)
    termination_date = Column(Date)
    
    active = Column(Boolean, default=True, index=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_pt_ins_patient', 'patient_id'),
    )


class InsuranceClaim(Base):
    """Insurance claims"""
    __tablename__ = 'insurance_claims'
    
    claim_id = Column(String(36), primary_key=True)
    patient_id = Column(String(36), ForeignKey('patients.patient_id'), nullable=False, index=True)
    patient_insurance_id = Column(String(36), ForeignKey('patient_insurance.patient_insurance_id'))
    
    # Service
    service_date = Column(Date, nullable=False, index=True)
    provider_id = Column(String(36), ForeignKey('providers.provider_id'), nullable=False)
    facility_id = Column(String(36))
    
    # Codes
    diagnosis_codes = Column(JSON, nullable=False)  # ICD-10
    procedure_codes = Column(JSON, nullable=False)  # CPT/HCPCS
    
    # Amounts
    billed_amount = Column(Float, nullable=False)
    allowed_amount = Column(Float)
    paid_amount = Column(Float)
    patient_responsibility = Column(Float)
    
    # Status
    status = Column(SQLEnum(ClaimStatusEnum), nullable=False, default=ClaimStatusEnum.DRAFT, index=True)
    
    # Dates
    submission_date = Column(DateTime)
    adjudication_date = Column(DateTime)
    payment_date = Column(DateTime)
    
    # Denial
    denial_reason = Column(Text)
    appeal_deadline = Column(Date)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_claim_patient_date', 'patient_id', 'service_date'),
        Index('idx_claim_status', 'status'),
    )


# ============================================================================
# PAYMENTS
# ============================================================================

class Payment(Base):
    """Payment transactions"""
    __tablename__ = 'payments'
    
    payment_id = Column(String(36), primary_key=True)
    patient_id = Column(String(36), ForeignKey('patients.patient_id'), nullable=False, index=True)
    
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default='USD')
    
    payment_method = Column(String(50), nullable=False)
    payment_status = Column(String(20), nullable=False, default='pending', index=True)
    
    # References
    claim_id = Column(String(36), ForeignKey('insurance_claims.claim_id'))
    invoice_id = Column(String(36))
    
    # Payment processor
    transaction_id = Column(String(100))
    processor = Column(String(50))  # stripe, square, etc.
    
    # Dates
    payment_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    processed_date = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_payment_patient', 'patient_id'),
        Index('idx_payment_status', 'payment_status'),
    )


# ============================================================================
# TELEMEDICINE
# ============================================================================

class TelehealthSession(Base):
    """Telehealth video sessions"""
    __tablename__ = 'telehealth_sessions'
    
    session_id = Column(String(36), primary_key=True)
    appointment_id = Column(String(36), ForeignKey('appointments.appointment_id'), nullable=False)
    patient_id = Column(String(36), ForeignKey('patients.patient_id'), nullable=False, index=True)
    provider_id = Column(String(36), ForeignKey('providers.provider_id'), nullable=False, index=True)
    
    # Schedule
    scheduled_start = Column(DateTime, nullable=False)
    scheduled_end = Column(DateTime, nullable=False)
    
    # Actual
    actual_start = Column(DateTime)
    actual_end = Column(DateTime)
    
    # Video
    video_url = Column(String(500), nullable=False)
    recording_url = Column(String(500))
    record_session = Column(Boolean, default=False)
    
    # Status
    status = Column(String(20), default='scheduled')
    
    # Participants
    patient_joined = Column(Boolean, default=False)
    provider_joined = Column(Boolean, default=False)
    patient_join_time = Column(DateTime)
    provider_join_time = Column(DateTime)
    
    # Quality
    connection_quality = Column(String(20))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_telehealth_appointment', 'appointment_id'),
    )


# ============================================================================
# ANALYTICS & AUDIT
# ============================================================================

class AuditLog(Base):
    """Comprehensive audit logging for HIPAA compliance"""
    __tablename__ = 'audit_logs'
    
    log_id = Column(String(36), primary_key=True)
    
    # Who
    user_id = Column(String(36), ForeignKey('users.user_id'), index=True)
    user_role = Column(String(20))
    
    # What
    action = Column(String(100), nullable=False, index=True)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(String(36), index=True)
    
    # When
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Where
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    
    # Details
    changes = Column(JSON)  # Before/after values
    
    # PHI access
    phi_accessed = Column(Boolean, default=False, index=True)
    patient_id = Column(String(36), ForeignKey('patients.patient_id'), index=True)
    
    __table_args__ = (
        Index('idx_audit_timestamp', 'timestamp'),
        Index('idx_audit_user', 'user_id', 'timestamp'),
        Index('idx_audit_resource', 'resource_type', 'resource_id'),
    )


# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def init_database(connection_string: str = "postgresql://localhost/aurora_health"):
    """Initialize database and create all tables"""
    
    engine = create_engine(connection_string)
    Base.metadata.create_all(engine)
    
    print("✅ Database initialized successfully")
    print(f"   Created {len(Base.metadata.tables)} tables")
    
    return engine


def get_session(engine):
    """Get database session"""
    Session = sessionmaker(bind=engine)
    return Session()


if __name__ == "__main__":
    # Initialize database
    engine = init_database()
    
    print("\nDatabase schema:")
    for table_name in Base.metadata.tables:
        print(f"  - {table_name}")
