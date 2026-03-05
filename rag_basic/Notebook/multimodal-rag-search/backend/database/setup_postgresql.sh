#!/bin/bash
# 🐘 Aurora Health - PostgreSQL Setup & Installation Script
# Automatic installation, database creation, and data initialization

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DB_NAME="aurora_health"
DB_USER="aurora"
DB_PASSWORD="aurora_secure_password_2026"
DB_PORT="5432"

echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                          ║${NC}"
echo -e "${BLUE}║  🐘 PostgreSQL Setup for Aurora Health                  ║${NC}"
echo -e "${BLUE}║                                                          ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Function to check if PostgreSQL is installed
check_postgres_installed() {
    print_info "Checking if PostgreSQL is installed..."
    
    if command -v psql &> /dev/null; then
        PSQL_VERSION=$(psql --version | awk '{print $3}')
        print_success "PostgreSQL is already installed (version: $PSQL_VERSION)"
        return 0
    else
        print_warning "PostgreSQL is not installed"
        return 1
    fi
}

# Function to install PostgreSQL
install_postgres() {
    print_info "Installing PostgreSQL..."
    
    # Detect OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if [ -f /etc/debian_version ]; then
            # Debian/Ubuntu
            print_info "Detected Debian/Ubuntu system"
            
            sudo apt-get update
            sudo apt-get install -y postgresql postgresql-contrib
            
        elif [ -f /etc/redhat-release ]; then
            # RedHat/CentOS/Fedora
            print_info "Detected RedHat/CentOS/Fedora system"
            
            sudo yum install -y postgresql-server postgresql-contrib
            sudo postgresql-setup initdb
            
        else
            print_error "Unsupported Linux distribution"
            exit 1
        fi
        
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        print_info "Detected macOS system"
        
        if command -v brew &> /dev/null; then
            brew install postgresql@15
            brew services start postgresql@15
        else
            print_error "Homebrew not found. Please install Homebrew first:"
            print_info "Visit: https://brew.sh"
            exit 1
        fi
        
    else
        print_error "Unsupported operating system: $OSTYPE"
        exit 1
    fi
    
    print_success "PostgreSQL installed successfully"
}

# Function to start PostgreSQL service
start_postgres() {
    print_info "Starting PostgreSQL service..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo systemctl start postgresql
        sudo systemctl enable postgresql
        print_success "PostgreSQL service started and enabled"
        
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew services start postgresql@15
        print_success "PostgreSQL service started"
    fi
}

# Function to check if PostgreSQL is running
check_postgres_running() {
    print_info "Checking if PostgreSQL is running..."
    
    if pg_isready -q; then
        print_success "PostgreSQL is running"
        return 0
    else
        print_warning "PostgreSQL is not running"
        return 1
    fi
}

# Function to create database user
create_db_user() {
    print_info "Creating database user: $DB_USER..."
    
    # Check if user already exists
    USER_EXISTS=$(sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'")
    
    if [ "$USER_EXISTS" = "1" ]; then
        print_warning "User $DB_USER already exists"
    else
        sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
        sudo -u postgres psql -c "ALTER USER $DB_USER CREATEDB;"
        print_success "User $DB_USER created"
    fi
}

# Function to create database
create_database() {
    print_info "Creating database: $DB_NAME..."
    
    # Check if database already exists
    DB_EXISTS=$(sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -w $DB_NAME | wc -l)
    
    if [ $DB_EXISTS -eq 1 ]; then
        print_warning "Database $DB_NAME already exists"
    else
        sudo -u postgres psql -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"
        print_success "Database $DB_NAME created"
    fi
    
    # Grant privileges
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
    print_success "Privileges granted to $DB_USER"
}

# Function to create tables
create_tables() {
    print_info "Creating database tables..."
    
    # Create SQL script
    cat > /tmp/create_tables.sql << 'EOF'
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(50) NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Patients table
CREATE TABLE IF NOT EXISTS patients (
    patient_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(20) NOT NULL,
    blood_type VARCHAR(5),
    address_street VARCHAR(255),
    address_city VARCHAR(100),
    address_district VARCHAR(100),
    address_division VARCHAR(100),
    emergency_contact_name VARCHAR(255),
    emergency_contact_phone VARCHAR(20),
    allergies JSONB,
    chronic_conditions JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Hospitals table
CREATE TABLE IF NOT EXISTS hospitals (
    hospital_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    name_bengali VARCHAR(255),
    hospital_type VARCHAR(50) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    address TEXT NOT NULL,
    district VARCHAR(100) NOT NULL,
    division VARCHAR(100) NOT NULL,
    phone_emergency VARCHAR(20),
    phone_general VARCHAR(20),
    email VARCHAR(255),
    total_beds INTEGER DEFAULT 0,
    departments JSONB,
    equipment JSONB,
    quality_rating DECIMAL(3, 2) DEFAULT 0.0,
    emergency_24x7 BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bed availability table
CREATE TABLE IF NOT EXISTS bed_availability (
    availability_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    hospital_id UUID REFERENCES hospitals(hospital_id) ON DELETE CASCADE,
    bed_type VARCHAR(20) NOT NULL,
    total_beds INTEGER NOT NULL,
    occupied INTEGER DEFAULT 0,
    available INTEGER DEFAULT 0,
    reserved INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Emergency cases table
CREATE TABLE IF NOT EXISTS emergency_cases (
    case_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID REFERENCES patients(patient_id),
    chief_complaint TEXT NOT NULL,
    symptoms JSONB,
    severity INTEGER CHECK (severity BETWEEN 1 AND 10),
    urgency VARCHAR(20) NOT NULL,
    ai_diagnosis JSONB,
    patient_latitude DECIMAL(10, 8),
    patient_longitude DECIMAL(11, 8),
    patient_address TEXT,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);

-- Ambulance dispatches table
CREATE TABLE IF NOT EXISTS ambulance_dispatches (
    dispatch_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID REFERENCES emergency_cases(case_id),
    ambulance_type VARCHAR(50) NOT NULL,
    vehicle_number VARCHAR(50),
    driver_name VARCHAR(255),
    driver_phone VARCHAR(20),
    pickup_latitude DECIMAL(10, 8),
    pickup_longitude DECIMAL(11, 8),
    hospital_id UUID REFERENCES hospitals(hospital_id),
    status VARCHAR(20) DEFAULT 'dispatched',
    eta_minutes INTEGER,
    cost INTEGER,
    dispatched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    arrived_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- Bed bookings table
CREATE TABLE IF NOT EXISTS bed_bookings (
    booking_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    hospital_id UUID REFERENCES hospitals(hospital_id),
    patient_id UUID REFERENCES patients(patient_id),
    bed_type VARCHAR(20) NOT NULL,
    bed_number VARCHAR(20),
    admission_date TIMESTAMP NOT NULL,
    estimated_days INTEGER,
    status VARCHAR(20) DEFAULT 'confirmed',
    advance_payment INTEGER,
    total_cost INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Admissions table
CREATE TABLE IF NOT EXISTS admissions (
    admission_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    booking_id UUID REFERENCES bed_bookings(booking_id),
    patient_id UUID REFERENCES patients(patient_id),
    hospital_id UUID REFERENCES hospitals(hospital_id),
    admission_number VARCHAR(50) UNIQUE,
    bed_number VARCHAR(20),
    ward VARCHAR(100),
    attending_physician VARCHAR(255),
    admission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    discharge_date TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit log table (for HIPAA compliance)
CREATE TABLE IF NOT EXISTS audit_logs (
    log_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id UUID,
    patient_id UUID REFERENCES patients(patient_id),
    ip_address VARCHAR(45),
    changes JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_patients_user_id ON patients(user_id);
CREATE INDEX IF NOT EXISTS idx_hospitals_district ON hospitals(district);
CREATE INDEX IF NOT EXISTS idx_hospitals_type ON hospitals(hospital_type);
CREATE INDEX IF NOT EXISTS idx_bed_availability_hospital ON bed_availability(hospital_id);
CREATE INDEX IF NOT EXISTS idx_emergency_cases_status ON emergency_cases(status);
CREATE INDEX IF NOT EXISTS idx_emergency_cases_created ON emergency_cases(created_at);
CREATE INDEX IF NOT EXISTS idx_ambulance_status ON ambulance_dispatches(status);
CREATE INDEX IF NOT EXISTS idx_bed_bookings_hospital ON bed_bookings(hospital_id);
CREATE INDEX IF NOT EXISTS idx_admissions_patient ON admissions(patient_id);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp);

COMMENT ON TABLE users IS 'All system users (patients, doctors, nurses, admins)';
COMMENT ON TABLE patients IS 'Patient demographic and medical information';
COMMENT ON TABLE hospitals IS 'Hospital directory with locations and capabilities';
COMMENT ON TABLE bed_availability IS 'Real-time bed availability tracking';
COMMENT ON TABLE emergency_cases IS 'Critical patient cases requiring emergency care';
COMMENT ON TABLE ambulance_dispatches IS 'Ambulance dispatch tracking';
COMMENT ON TABLE bed_bookings IS 'Hospital bed reservations';
COMMENT ON TABLE admissions IS 'Patient hospital admissions';
COMMENT ON TABLE audit_logs IS 'HIPAA-compliant audit trail';

EOF

    # Execute SQL script
    PGPASSWORD=$DB_PASSWORD psql -h localhost -U $DB_USER -d $DB_NAME -f /tmp/create_tables.sql
    
    if [ $? -eq 0 ]; then
        print_success "Database tables created successfully"
    else
        print_error "Failed to create tables"
        exit 1
    fi
    
    # Clean up
    rm /tmp/create_tables.sql
}

# Function to insert sample data
insert_sample_data() {
    print_info "Inserting sample data..."
    
    # Create SQL script for sample data
    cat > /tmp/insert_data.sql << 'EOF'
-- Sample Users
INSERT INTO users (user_id, email, password_hash, full_name, phone, role, email_verified)
VALUES 
    ('11111111-1111-1111-1111-111111111111', 'patient1@example.com', 'hashed_password_1', 'Mohammad Rahman', '+880 1711-123456', 'patient', TRUE),
    ('22222222-2222-2222-2222-222222222222', 'patient2@example.com', 'hashed_password_2', 'Fatima Begum', '+880 1812-234567', 'patient', TRUE),
    ('33333333-3333-3333-3333-333333333333', 'doctor1@example.com', 'hashed_password_3', 'Dr. Abdul Karim', '+880 1913-345678', 'doctor', TRUE),
    ('44444444-4444-4444-4444-444444444444', 'admin1@example.com', 'hashed_password_4', 'Admin User', '+880 1714-456789', 'admin', TRUE)
ON CONFLICT (email) DO NOTHING;

-- Sample Patients
INSERT INTO patients (patient_id, user_id, date_of_birth, gender, blood_type, address_city, address_district, address_division, emergency_contact_name, emergency_contact_phone, allergies, chronic_conditions)
VALUES 
    ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '11111111-1111-1111-1111-111111111111', '1970-05-15', 'male', 'B+', 'Dhaka', 'Dhaka', 'Dhaka', 'Ayesha Rahman', '+880 1812-111111', '["Penicillin"]', '["Hypertension", "Type 2 Diabetes"]'),
    ('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', '22222222-2222-2222-2222-222222222222', '1985-08-22', 'female', 'O+', 'Chittagong', 'Chittagong', 'Chittagong', 'Ahmed Begum', '+880 1913-222222', '["Latex"]', '["Asthma"]')
ON CONFLICT (user_id) DO NOTHING;

-- Sample Hospitals (Major Bangladesh Hospitals)
INSERT INTO hospitals (hospital_id, name, name_bengali, hospital_type, latitude, longitude, address, district, division, phone_emergency, phone_general, total_beds, departments, equipment, quality_rating, emergency_24x7)
VALUES 
    (
        'cccccccc-cccc-cccc-cccc-cccccccccccc',
        'National Institute of Cardiovascular Diseases (NICVD)',
        'জাতীয় হৃদরোগ ইনস্টিটিউট',
        'govt_tertiary',
        23.7691,
        90.3684,
        'Sher-e-Bangla Nagar, Dhaka-1207',
        'Dhaka',
        'Dhaka',
        '02-9015951',
        '02-9015950',
        550,
        '["Cardiology", "Cardiac Surgery", "Interventional Cardiology", "Critical Care"]',
        '["Cath Lab", "Echo", "ECG", "Stress Test", "ICU Ventilators", "IABP", "ECMO"]',
        4.3,
        TRUE
    ),
    (
        'dddddddd-dddd-dddd-dddd-dddddddddddd',
        'Square Hospitals Ltd',
        'স্কয়ার হাসপাতাল লিমিটেড',
        'private_super',
        23.7516,
        90.3892,
        '18/F, Bir Uttam Qazi Nuruzzaman Sarak, West Panthapath, Dhaka-1205',
        'Dhaka',
        'Dhaka',
        '+880-2-8159457',
        '+880-2-48814916',
        400,
        '["Cardiology", "Neurology", "Oncology", "Orthopedics", "Gastroenterology", "Nephrology", "Urology", "ENT", "General Surgery", "Pediatrics", "Obstetrics"]',
        '["MRI 3T", "CT 256-slice", "Cath Lab", "Gamma Knife", "Linear Accelerator", "PET-CT", "ICU Ventilators"]',
        4.7,
        TRUE
    ),
    (
        'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee',
        'Dhaka Medical College Hospital (DMCH)',
        'ঢাকা মেডিকেল কলেজ হাসপাতাল',
        'govt_tertiary',
        23.7264,
        90.3984,
        'Secretariat Road, Dhaka-1000',
        'Dhaka',
        'Dhaka',
        '02-9668690',
        '02-9668690',
        2600,
        '["Medicine", "Surgery", "Orthopedics", "Gynecology", "Pediatrics", "Neurology", "Cardiology", "Emergency"]',
        '["CT Scan", "X-ray", "Ultrasound", "ICU", "Ventilators", "Blood Bank", "Laboratory"]',
        3.8,
        TRUE
    )
ON CONFLICT (hospital_id) DO NOTHING;

-- Sample Bed Availability
INSERT INTO bed_availability (hospital_id, bed_type, total_beds, occupied, available, reserved)
VALUES 
    ('cccccccc-cccc-cccc-cccc-cccccccccccc', 'icu', 80, 78, 2, 1),
    ('cccccccc-cccc-cccc-cccc-cccccccccccc', 'ccu', 20, 18, 2, 0),
    ('cccccccc-cccc-cccc-cccc-cccccccccccc', 'cabin', 150, 135, 15, 5),
    ('cccccccc-cccc-cccc-cccc-cccccccccccc', 'ward', 300, 275, 25, 10),
    ('dddddddd-dddd-dddd-dddd-dddddddddddd', 'icu', 60, 57, 3, 2),
    ('dddddddd-dddd-dddd-dddd-dddddddddddd', 'cabin', 150, 138, 12, 8),
    ('dddddddd-dddd-dddd-dddd-dddddddddddd', 'ward', 150, 142, 8, 5),
    ('eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee', 'icu', 100, 98, 2, 1),
    ('eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee', 'cabin', 250, 235, 15, 10),
    ('eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee', 'ward', 2200, 2150, 50, 30)
ON CONFLICT DO NOTHING;

-- Sample Emergency Case
INSERT INTO emergency_cases (case_id, patient_id, chief_complaint, symptoms, severity, urgency, ai_diagnosis, patient_latitude, patient_longitude, patient_address, status)
VALUES 
    (
        'ffffffff-ffff-ffff-ffff-ffffffffffff',
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
        'Severe chest pain, sweating, shortness of breath',
        '["chest_pain", "sweating", "dyspnea", "nausea"]',
        9,
        'immediate',
        '[{"disease": "Acute Myocardial Infarction (STEMI)", "probability": 0.85, "specialist": "Cardiologist"}]',
        23.8617,
        90.0003,
        'Village: Char Manikdi, Manikganj Sadar, Manikganj',
        'active'
    )
ON CONFLICT DO NOTHING;

EOF

    # Execute SQL script
    PGPASSWORD=$DB_PASSWORD psql -h localhost -U $DB_USER -d $DB_NAME -f /tmp/insert_data.sql
    
    if [ $? -eq 0 ]; then
        print_success "Sample data inserted successfully"
    else
        print_error "Failed to insert sample data"
        exit 1
    fi
    
    # Clean up
    rm /tmp/insert_data.sql
}

# Function to test database connection
test_connection() {
    print_info "Testing database connection..."
    
    # Test connection
    PGPASSWORD=$DB_PASSWORD psql -h localhost -U $DB_USER -d $DB_NAME -c "SELECT version();" > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        print_success "Database connection successful!"
        
        # Show database info
        echo ""
        print_info "Database Information:"
        echo "  Database: $DB_NAME"
        echo "  User: $DB_USER"
        echo "  Host: localhost"
        echo "  Port: $DB_PORT"
        echo ""
        
        # Show table count
        TABLE_COUNT=$(PGPASSWORD=$DB_PASSWORD psql -h localhost -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';")
        print_info "Total tables created: $TABLE_COUNT"
        
        # Show sample data counts
        echo ""
        print_info "Sample data counts:"
        USER_COUNT=$(PGPASSWORD=$DB_PASSWORD psql -h localhost -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM users;")
        echo "  Users: $USER_COUNT"
        
        HOSPITAL_COUNT=$(PGPASSWORD=$DB_PASSWORD psql -h localhost -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM hospitals;")
        echo "  Hospitals: $HOSPITAL_COUNT"
        
        BED_COUNT=$(PGPASSWORD=$DB_PASSWORD psql -h localhost -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM bed_availability;")
        echo "  Bed availability records: $BED_COUNT"
        
    else
        print_error "Database connection failed!"
        exit 1
    fi
}

# Function to create connection string file
create_connection_file() {
    print_info "Creating database connection configuration..."
    
    # Create .env file
    cat > database.env << EOF
# Aurora Health - PostgreSQL Connection Configuration
# Generated: $(date)

DB_HOST=localhost
DB_PORT=$DB_PORT
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD

# Connection string
DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@localhost:$DB_PORT/$DB_NAME

# SQLAlchemy connection string
SQLALCHEMY_DATABASE_URI=postgresql://$DB_USER:$DB_PASSWORD@localhost:$DB_PORT/$DB_NAME
EOF

    print_success "Connection configuration saved to database.env"
    
    # Create Python connection example
    cat > test_connection.py << 'PYEOF'
#!/usr/bin/env python3
"""
Test PostgreSQL connection
"""

import os
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv('database.env')

def test_psycopg2():
    """Test connection with psycopg2"""
    print("Testing connection with psycopg2...")
    
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        
        cursor = conn.cursor()
        cursor.execute('SELECT version();')
        version = cursor.fetchone()
        
        print(f"✅ Connection successful!")
        print(f"   PostgreSQL version: {version[0]}")
        
        # Test query
        cursor.execute('SELECT COUNT(*) FROM hospitals;')
        count = cursor.fetchone()[0]
        print(f"   Hospitals in database: {count}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


def test_sqlalchemy():
    """Test connection with SQLAlchemy"""
    print("\nTesting connection with SQLAlchemy...")
    
    try:
        database_url = os.getenv('SQLALCHEMY_DATABASE_URI')
        engine = create_engine(database_url)
        
        with engine.connect() as connection:
            result = connection.execute(text('SELECT version();'))
            version = result.fetchone()[0]
            
            print(f"✅ Connection successful!")
            print(f"   PostgreSQL version: {version}")
            
            # Test query
            result = connection.execute(text('SELECT COUNT(*) FROM users;'))
            count = result.fetchone()[0]
            print(f"   Users in database: {count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


if __name__ == "__main__":
    print("🐘 Aurora Health - PostgreSQL Connection Test\n")
    
    success = True
    success = test_psycopg2() and success
    success = test_sqlalchemy() and success
    
    if success:
        print("\n✅ All connection tests passed!")
    else:
        print("\n❌ Some connection tests failed")
        exit(1)
PYEOF

    chmod +x test_connection.py
    print_success "Python test script created: test_connection.py"
}

# Main installation flow
main() {
    echo ""
    print_info "Starting PostgreSQL setup process..."
    echo ""
    
    # Step 1: Check if PostgreSQL is installed
    if ! check_postgres_installed; then
        read -p "PostgreSQL is not installed. Install now? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            install_postgres
        else
            print_error "PostgreSQL installation cancelled"
            exit 1
        fi
    fi
    
    # Step 2: Start PostgreSQL service
    if ! check_postgres_running; then
        start_postgres
        sleep 3  # Wait for service to start
        
        if ! check_postgres_running; then
            print_error "Failed to start PostgreSQL service"
            exit 1
        fi
    fi
    
    # Step 3: Create database user
    create_db_user
    
    # Step 4: Create database
    create_database
    
    # Step 5: Create tables
    create_tables
    
    # Step 6: Insert sample data
    read -p "Insert sample data? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        insert_sample_data
    fi
    
    # Step 7: Test connection
    test_connection
    
    # Step 8: Create connection configuration
    create_connection_file
    
    # Success message
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                          ║${NC}"
    echo -e "${GREEN}║  ✅ PostgreSQL Setup Complete!                          ║${NC}"
    echo -e "${GREEN}║                                                          ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    print_info "Next steps:"
    echo "  1. Review connection details in: database.env"
    echo "  2. Test Python connection: python3 test_connection.py"
    echo "  3. Connect with psql: psql -U $DB_USER -d $DB_NAME"
    echo "  4. View tables: psql -U $DB_USER -d $DB_NAME -c '\\dt'"
    echo ""
    
    print_warning "Security reminder:"
    echo "  - Change the default password in production!"
    echo "  - Restrict network access to PostgreSQL"
    echo "  - Enable SSL/TLS for connections"
    echo "  - Regular backups are essential"
    echo ""
}

# Run main function
main
