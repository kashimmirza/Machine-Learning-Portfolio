# backend/databases/medical_knowledge_base.py
"""
Medical Knowledge Base Database
SQLite database with medical terminology, drugs, diseases, guidelines
"""

import sqlite3
import json
from typing import List, Dict, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class MedicalKnowledgeBase:
    """Medical knowledge database"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Create in user data directory
            db_dir = Path("/mnt/user-data/outputs/data")
            db_dir.mkdir(parents=True, exist_ok=True)
            db_path = str(db_dir / "medical_kb.db")
        
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._initialize_tables()
        self._load_initial_data()
        logger.info(f"Medical KB initialized: {db_path}")
    
    def _initialize_tables(self):
        """Create database schema"""
        cursor = self.conn.cursor()
        
        # Diseases
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS diseases (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                icd10_code TEXT,
                description TEXT,
                symptoms TEXT,
                risk_factors TEXT,
                prevalence REAL,
                mortality_rate REAL,
                typical_onset_age INTEGER
            )
        """)
        
        # Medications
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medications (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                generic_name TEXT,
                drug_class TEXT,
                indications TEXT,
                contraindications TEXT,
                side_effects TEXT,
                interactions TEXT,
                dosing TEXT,
                pregnancy_category TEXT,
                fda_approved BOOLEAN
            )
        """)
        
        # Symptoms
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS symptoms (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                severity_levels TEXT,
                associated_diseases TEXT,
                red_flags TEXT
            )
        """)
        
        self.conn.commit()
    
    def _load_initial_data(self):
        """Load initial medical data"""
        cursor = self.conn.cursor()
        
        # Check if data exists
        cursor.execute("SELECT COUNT(*) FROM diseases")
        if cursor.fetchone()[0] > 0:
            return
        
        # Load diseases
        diseases = [
            ('Hypertension', 'I10', 'High blood pressure', 
             json.dumps(['headache', 'dizziness']),
             json.dumps(['age', 'obesity', 'smoking']), 0.32, None, 45),
            
            ('Type 2 Diabetes', 'E11', 'Metabolic disorder',
             json.dumps(['polyuria', 'polydipsia', 'fatigue']),
             json.dumps(['obesity', 'family_history']), 0.13, None, 50),
            
            ('Pneumonia', 'J18.9', 'Lung infection',
             json.dumps(['cough', 'fever', 'chest_pain']),
             json.dumps(['age>65', 'smoking']), 0.005, 0.05, 65),
            
            ('Heart Attack', 'I21', 'Myocardial infarction',
             json.dumps(['chest_pain', 'dyspnea', 'nausea']),
             json.dumps(['hypertension', 'diabetes', 'smoking']), 0.003, 0.10, 65),
            
            ('Melanoma', 'C43', 'Skin cancer',
             json.dumps(['changing_mole', 'irregular_borders']),
             json.dumps(['sun_exposure', 'fair_skin']), 0.0002, 0.15, 55)
        ]
        
        cursor.executemany("""
            INSERT INTO diseases (name, icd10_code, description, symptoms,
                                 risk_factors, prevalence, mortality_rate, typical_onset_age)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, diseases)
        
        # Load medications
        medications = [
            ('Lisinopril', 'Lisinopril', 'ACE Inhibitor',
             json.dumps(['hypertension', 'heart_failure']),
             json.dumps(['pregnancy', 'angioedema_history']),
             json.dumps(['cough', 'hypotension']),
             json.dumps(['NSAIDs', 'potassium_supplements']),
             json.dumps({'initial': '10mg daily', 'max': '40mg daily'}),
             'D', True),
            
            ('Metformin', 'Metformin', 'Biguanide',
             json.dumps(['type_2_diabetes']),
             json.dumps(['renal_impairment', 'liver_disease']),
             json.dumps(['GI_upset', 'diarrhea']),
             json.dumps(['contrast_dye', 'alcohol']),
             json.dumps({'initial': '500mg twice daily', 'max': '2000mg daily'}),
             'B', True),
            
            ('Aspirin', 'Acetylsalicylic Acid', 'Antiplatelet',
             json.dumps(['cardiovascular_prevention', 'acute_MI']),
             json.dumps(['bleeding_disorder', 'active_GI_bleed']),
             json.dumps(['GI_bleeding', 'bruising']),
             json.dumps(['warfarin', 'NSAIDs']),
             json.dumps({'prevention': '81mg daily', 'acute_MI': '325mg stat'}),
             'C', True)
        ]
        
        cursor.executemany("""
            INSERT INTO medications (name, generic_name, drug_class, indications,
                                    contraindications, side_effects, interactions,
                                    dosing, pregnancy_category, fda_approved)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, medications)
        
        self.conn.commit()
        logger.info("Initial medical data loaded")
    
    def query_diseases(self, symptoms: List[str]) -> List[Dict]:
        """Find diseases matching symptoms"""
        cursor = self.conn.cursor()
        results = []
        
        for symptom in symptoms:
            cursor.execute("""
                SELECT * FROM diseases 
                WHERE symptoms LIKE ?
                ORDER BY prevalence DESC
                LIMIT 10
            """, (f'%{symptom}%',))
            
            for row in cursor.fetchall():
                results.append({
                    'name': row[1],
                    'icd10': row[2],
                    'description': row[3],
                    'prevalence': row[6]
                })
        
        return results
    
    def check_drug_interactions(self, medications: List[str]) -> List[Dict]:
        """Check for drug-drug interactions"""
        cursor = self.conn.cursor()
        interactions = []
        
        for i, med1 in enumerate(medications):
            for med2 in medications[i+1:]:
                cursor.execute("""
                    SELECT m1.name, m2.name, m1.interactions
                    FROM medications m1, medications m2
                    WHERE m1.name = ? AND m2.name = ?
                """, (med1, med2))
                
                result = cursor.fetchone()
                if result and result[2]:
                    interactions_list = json.loads(result[2])
                    if med2.lower() in [i.lower() for i in interactions_list]:
                        interactions.append({
                            'drug1': med1,
                            'drug2': med2,
                            'severity': 'moderate',
                            'description': f'{med1} may interact with {med2}'
                        })
        
        return interactions
    
    def get_clinical_guideline(self, condition: str) -> Dict:
        """Get clinical practice guideline"""
        # Placeholder - in production, query guidelines database
        return {
            'title': f'Guidelines for {condition}',
            'organization': 'Medical Society',
            'recommendations': [
                'Follow standard of care',
                'Monitor patient response',
                'Adjust treatment as needed'
            ],
            'evidence_level': 'A',
            'source': 'Clinical guidelines database'
        }


# Singleton
_medical_kb = None

def get_medical_kb() -> MedicalKnowledgeBase:
    global _medical_kb
    if _medical_kb is None:
        _medical_kb = MedicalKnowledgeBase()
    return _medical_kb
