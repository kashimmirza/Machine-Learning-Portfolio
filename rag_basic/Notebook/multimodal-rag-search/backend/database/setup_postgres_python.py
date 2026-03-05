#!/usr/bin/env python3
"""
🐘 Aurora Health - PostgreSQL Setup & Testing (Python)
Complete database setup, connection testing, and data manipulation

Usage:
    python3 setup_postgres_python.py
"""

import os
import sys
import subprocess
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import getpass
from datetime import datetime

# Configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'aurora_health',
    'user': 'aurora',
    'password': 'aurora_secure_password_2026'
}


class Colors:
    """Terminal colors"""
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    NC = '\033[0m'  # No Color


def print_header(text):
    """Print header"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.NC}")
    print(f"{Colors.BLUE}{text.center(60)}{Colors.NC}")
    print(f"{Colors.BLUE}{'='*60}{Colors.NC}\n")


def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.NC}")


def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}❌ {text}{Colors.NC}")


def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.NC}")


def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.NC}")


def check_postgres_installed():
    """Check if PostgreSQL is installed"""
    print_info("Checking if PostgreSQL is installed...")
    
    try:
        result = subprocess.run(
            ['psql', '--version'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            version = result.stdout.strip()
            print_success(f"PostgreSQL installed: {version}")
            return True
        else:
            print_error("PostgreSQL not installed")
            return False
            
    except FileNotFoundError:
        print_error("PostgreSQL not found in PATH")
        return False


def check_postgres_running():
    """Check if PostgreSQL is running"""
    print_info("Checking if PostgreSQL is running...")
    
    try:
        result = subprocess.run(
            ['pg_isready'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print_success("PostgreSQL is running")
            return True
        else:
            print_error("PostgreSQL is not running")
            return False
            
    except FileNotFoundError:
        print_error("pg_isready command not found")
        return False


def create_database():
    """Create database if not exists"""
    print_info(f"Creating database: {DB_CONFIG['database']}...")
    
    try:
        # Connect to default postgres database
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            database='postgres',
            user='postgres'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (DB_CONFIG['database'],)
        )
        
        if cursor.fetchone():
            print_warning(f"Database {DB_CONFIG['database']} already exists")
        else:
            # Create database
            cursor.execute(
                sql.SQL("CREATE DATABASE {} OWNER {}").format(
                    sql.Identifier(DB_CONFIG['database']),
                    sql.Identifier(DB_CONFIG['user'])
                )
            )
            print_success(f"Database {DB_CONFIG['database']} created")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print_error(f"Failed to create database: {e}")
        return False


def test_connection():
    """Test database connection"""
    print_info("Testing database connection...")
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Get PostgreSQL version
        cursor.execute('SELECT version();')
        version = cursor.fetchone()[0]
        
        print_success("Connection successful!")
        print_info(f"PostgreSQL version: {version.split(',')[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print_error(f"Connection failed: {e}")
        return False


def create_tables():
    """Create database tables"""
    print_info("Creating database tables...")
    
    create_table_sql = """
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
        address_city VARCHAR(100),
        address_district VARCHAR(100),
        emergency_contact_name VARCHAR(255),
        emergency_contact_phone VARCHAR(20),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Hospitals table
    CREATE TABLE IF NOT EXISTS hospitals (
        hospital_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        name VARCHAR(255) NOT NULL,
        name_bengali VARCHAR(255),
        hospital_type VARCHAR(50),
        latitude DECIMAL(10, 8),
        longitude DECIMAL(11, 8),
        address TEXT,
        district VARCHAR(100),
        phone_emergency VARCHAR(20),
        total_beds INTEGER DEFAULT 0,
        quality_rating DECIMAL(3, 2) DEFAULT 0.0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Bed availability table
    CREATE TABLE IF NOT EXISTS bed_availability (
        availability_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        hospital_id UUID REFERENCES hospitals(hospital_id),
        bed_type VARCHAR(20),
        total_beds INTEGER,
        available INTEGER DEFAULT 0,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Emergency cases table
    CREATE TABLE IF NOT EXISTS emergency_cases (
        case_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        patient_id UUID REFERENCES patients(patient_id),
        chief_complaint TEXT,
        severity INTEGER,
        urgency VARCHAR(20),
        status VARCHAR(20) DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Create indexes
    CREATE INDEX IF NOT EXISTS idx_patients_user ON patients(user_id);
    CREATE INDEX IF NOT EXISTS idx_hospitals_district ON hospitals(district);
    CREATE INDEX IF NOT EXISTS idx_bed_availability_hospital ON bed_availability(hospital_id);
    """
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute(create_table_sql)
        conn.commit()
        
        # Count tables
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema='public' AND table_type='BASE TABLE';
        """)
        table_count = cursor.fetchone()[0]
        
        print_success(f"Tables created successfully ({table_count} tables)")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print_error(f"Failed to create tables: {e}")
        return False


def insert_sample_data():
    """Insert sample data"""
    print_info("Inserting sample data...")
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Insert sample users
        cursor.execute("""
            INSERT INTO users (email, password_hash, full_name, phone, role, email_verified)
            VALUES 
                ('patient1@aurora.health', 'hashed_password', 'Mohammad Rahman', '+880 1711-123456', 'patient', TRUE),
                ('doctor1@aurora.health', 'hashed_password', 'Dr. Abdul Karim', '+880 1913-345678', 'doctor', TRUE)
            ON CONFLICT (email) DO NOTHING
            RETURNING user_id;
        """)
        
        users = cursor.fetchall()
        print_info(f"Inserted {len(users)} users")
        
        # Insert sample hospitals
        cursor.execute("""
            INSERT INTO hospitals (name, name_bengali, hospital_type, latitude, longitude, address, district, phone_emergency, total_beds, quality_rating)
            VALUES 
                ('NICVD', 'জাতীয় হৃদরোগ ইনস্টিটিউট', 'govt_tertiary', 23.7691, 90.3684, 'Sher-e-Bangla Nagar, Dhaka', 'Dhaka', '02-9015951', 550, 4.3),
                ('Square Hospitals', 'স্কয়ার হাসপাতাল', 'private_super', 23.7516, 90.3892, 'West Panthapath, Dhaka', 'Dhaka', '+880-2-8159457', 400, 4.7),
                ('DMCH', 'ঢাকা মেডিকেল কলেজ', 'govt_tertiary', 23.7264, 90.3984, 'Secretariat Road, Dhaka', 'Dhaka', '02-9668690', 2600, 3.8)
            RETURNING hospital_id;
        """)
        
        hospitals = cursor.fetchall()
        print_info(f"Inserted {len(hospitals)} hospitals")
        
        # Insert bed availability
        if hospitals:
            for hospital in hospitals:
                hospital_id = hospital[0]
                cursor.execute("""
                    INSERT INTO bed_availability (hospital_id, bed_type, total_beds, available)
                    VALUES 
                        (%s, 'icu', 50, 5),
                        (%s, 'cabin', 100, 20),
                        (%s, 'ward', 200, 45)
                    ON CONFLICT DO NOTHING;
                """, (hospital_id, hospital_id, hospital_id))
        
        conn.commit()
        
        # Count inserted data
        cursor.execute("SELECT COUNT(*) FROM users;")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM hospitals;")
        hospital_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM bed_availability;")
        bed_count = cursor.fetchone()[0]
        
        print_success(f"Sample data inserted:")
        print(f"  - Users: {user_count}")
        print(f"  - Hospitals: {hospital_count}")
        print(f"  - Bed records: {bed_count}")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print_error(f"Failed to insert sample data: {e}")
        return False


def query_sample_data():
    """Query and display sample data"""
    print_header("Sample Data Query")
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Query hospitals
        print_info("Hospitals in database:")
        cursor.execute("""
            SELECT name, name_bengali, district, total_beds, quality_rating 
            FROM hospitals 
            ORDER BY quality_rating DESC;
        """)
        
        hospitals = cursor.fetchall()
        for h in hospitals:
            print(f"  • {h[0]} ({h[1]})")
            print(f"    District: {h[2]} | Beds: {h[3]} | Rating: {h[4]}⭐")
        
        print()
        
        # Query bed availability
        print_info("Bed availability:")
        cursor.execute("""
            SELECT h.name, b.bed_type, b.total_beds, b.available
            FROM hospitals h
            JOIN bed_availability b ON h.hospital_id = b.hospital_id
            ORDER BY h.name, b.bed_type;
        """)
        
        beds = cursor.fetchall()
        current_hospital = None
        for b in beds:
            if b[0] != current_hospital:
                print(f"\n  {b[0]}:")
                current_hospital = b[0]
            print(f"    {b[1]}: {b[3]}/{b[2]} available")
        
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print_error(f"Query failed: {e}")


def save_connection_string():
    """Save connection string to file"""
    print_info("Saving connection configuration...")
    
    connection_string = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    
    with open('database_connection.txt', 'w') as f:
        f.write("# Aurora Health - PostgreSQL Connection\n")
        f.write(f"# Generated: {datetime.now()}\n\n")
        f.write(f"Host: {DB_CONFIG['host']}\n")
        f.write(f"Port: {DB_CONFIG['port']}\n")
        f.write(f"Database: {DB_CONFIG['database']}\n")
        f.write(f"User: {DB_CONFIG['user']}\n")
        f.write(f"Password: {DB_CONFIG['password']}\n\n")
        f.write(f"Connection String:\n{connection_string}\n\n")
        f.write(f"SQLAlchemy:\nSQLALCHEMY_DATABASE_URI = '{connection_string}'\n\n")
        f.write(f"Django:\nDATABASES = {{\n")
        f.write(f"    'default': {{\n")
        f.write(f"        'ENGINE': 'django.db.backends.postgresql',\n")
        f.write(f"        'NAME': '{DB_CONFIG['database']}',\n")
        f.write(f"        'USER': '{DB_CONFIG['user']}',\n")
        f.write(f"        'PASSWORD': '{DB_CONFIG['password']}',\n")
        f.write(f"        'HOST': '{DB_CONFIG['host']}',\n")
        f.write(f"        'PORT': '{DB_CONFIG['port']}',\n")
        f.write(f"    }}\n}}\n")
    
    print_success("Connection details saved to database_connection.txt")


def main():
    """Main setup process"""
    print_header("🐘 Aurora Health - PostgreSQL Setup")
    
    # Step 1: Check PostgreSQL
    if not check_postgres_installed():
        print_error("Please install PostgreSQL first:")
        print("  Ubuntu/Debian: sudo apt-get install postgresql postgresql-contrib")
        print("  macOS: brew install postgresql@15")
        print("  Windows: Download from https://www.postgresql.org/download/")
        sys.exit(1)
    
    if not check_postgres_running():
        print_error("PostgreSQL is not running. Start it:")
        print("  Linux: sudo systemctl start postgresql")
        print("  macOS: brew services start postgresql@15")
        sys.exit(1)
    
    print()
    
    # Step 2: Test connection
    if not test_connection():
        print_warning("Cannot connect with current credentials")
        print_info("You may need to:")
        print("  1. Create the user: sudo -u postgres createuser aurora")
        print("  2. Set password: sudo -u postgres psql -c \"ALTER USER aurora PASSWORD 'aurora_secure_password_2026';\"")
        sys.exit(1)
    
    print()
    
    # Step 3: Create database
    # create_database()  # Uncomment if needed
    print()
    
    # Step 4: Create tables
    if create_tables():
        print()
        
        # Step 5: Insert sample data
        response = input("Insert sample data? (y/n): ")
        if response.lower() == 'y':
            insert_sample_data()
            print()
            
            # Step 6: Query data
            query_sample_data()
    
    print()
    
    # Step 7: Save connection info
    save_connection_string()
    
    # Success
    print_header("✅ Setup Complete!")
    print_info("Next steps:")
    print("  1. Review connection details in: database_connection.txt")
    print("  2. Use connection string in your application")
    print("  3. Connect with psql: psql -U aurora -d aurora_health")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
