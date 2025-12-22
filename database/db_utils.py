"""
Database Utilities for SaarthiAI
Handles database connection, initialization, and sample data
"""

import sqlite3
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

DATABASE_PATH = 'database/saarthi.db'

def get_db_connection():
    """Get database connection with Row factory"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with all tables and sample data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'teacher', 'student', 'parent')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            student_id TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            date_of_birth DATE,
            gender TEXT,
            address TEXT,
            face_encoding BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Create Courses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_code TEXT UNIQUE NOT NULL,
            course_name TEXT NOT NULL,
            description TEXT,
            teacher_id INTEGER,
            semester TEXT,
            credits INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (teacher_id) REFERENCES users(id)
        )
    ''')
    
    # Create Enrollments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            enrollment_date DATE DEFAULT CURRENT_DATE,
            status TEXT DEFAULT 'active' CHECK(status IN ('active', 'dropped', 'completed')),
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (course_id) REFERENCES courses(id),
            UNIQUE(student_id, course_id)
        )
    ''')
    
    # Create Attendance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            date DATE NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('present', 'absent', 'late', 'excused')),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (course_id) REFERENCES courses(id),
            FOREIGN KEY (student_id) REFERENCES students(id),
            UNIQUE(course_id, student_id, date)
        )
    ''')
    
    # Create Parent-Student Link table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parent_student_link (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parent_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            relationship TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_id) REFERENCES users(id),
            FOREIGN KEY (student_id) REFERENCES students(id),
            UNIQUE(parent_id, student_id)
        )
    ''')
    
    # Create Fees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            total_amount DECIMAL(10, 2) NOT NULL,
            paid_amount DECIMAL(10, 2) DEFAULT 0,
            due_amount DECIMAL(10, 2) NOT NULL,
            due_date DATE,
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'partial', 'paid')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    ''')
    
    # Create Events table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            event_date DATE NOT NULL,
            event_time TIME,
            location TEXT,
            event_type TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    ''')
    
    # Create Announcements table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            priority TEXT DEFAULT 'normal' CHECK(priority IN ('low', 'normal', 'high')),
            target_audience TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    ''')
    
    # Create AI Chat History table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            response TEXT NOT NULL,
            chat_type TEXT DEFAULT 'general',
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    ''')
    
    # Create Assignments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            due_date DATE,
            max_marks INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    ''')
    
    conn.commit()
    
    # Insert sample data
    insert_sample_data(conn)
    
    conn.close()
    print("✅ Database initialized successfully!")

def insert_sample_data(conn):
    """Insert sample data for testing"""
    cursor = conn.cursor()
    
    # Check if data already exists
    existing_users = cursor.execute('SELECT COUNT(*) as count FROM users').fetchone()
    if existing_users['count'] > 0:
        print("ℹ️  Sample data already exists. Skipping...")
        return
    
    print("📝 Inserting sample data...")
    
    # Insert sample users
    users = [
        ('admin', generate_password_hash('admin123'), 'Admin User', 'admin@saarthi.ai', 'admin'),
        ('teacher1', generate_password_hash('teacher123'), 'Dr. Priya Sharma', 'priya.sharma@saarthi.ai', 'teacher'),
        ('student1', generate_password_hash('student123'), 'Aarav Singh', 'aarav.singh@student.saarthi.ai', 'student'),
        ('parent1', generate_password_hash('parent123'), 'Rajesh Kumar', 'rajesh.kumar@parent.saarthi.ai', 'parent'),
    ]
    
    cursor.executemany('''
        INSERT INTO users (username, password, full_name, email, role)
        VALUES (?, ?, ?, ?, ?)
    ''', users)
    
    # Get user IDs
    admin_id = cursor.execute("SELECT id FROM users WHERE username='admin'").fetchone()['id']
    teacher_id = cursor.execute("SELECT id FROM users WHERE username='teacher1'").fetchone()['id']
    student_user_id = cursor.execute("SELECT id FROM users WHERE username='student1'").fetchone()['id']
    parent_id = cursor.execute("SELECT id FROM users WHERE username='parent1'").fetchone()['id']
    
    # Insert sample students
    students = [
        (student_user_id, '2024001', 'Aarav', 'Singh', 'aarav.singh@student.saarthi.ai', '9876543210', '2006-05-15', 'Male', 'Mumbai, Maharashtra'),
        (None, '2024002', 'Diya', 'Patel', 'diya.patel@student.saarthi.ai', '9876543211', '2006-08-22', 'Female', 'Ahmedabad, Gujarat'),
        (None, '2024003', 'Rohan', 'Verma', 'rohan.verma@student.saarthi.ai', '9876543212', '2006-03-10', 'Male', 'Delhi, Delhi'),
    ]
    
    cursor.executemany('''
        INSERT INTO students (user_id, student_id, first_name, last_name, email, phone, date_of_birth, gender, address)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', students)
    
    # Get student IDs
    student1_id = cursor.execute("SELECT id FROM students WHERE student_id='2024001'").fetchone()['id']
    student2_id = cursor.execute("SELECT id FROM students WHERE student_id='2024002'").fetchone()['id']
    student3_id = cursor.execute("SELECT id FROM students WHERE student_id='2024003'").fetchone()['id']
    
    # Insert sample courses
    courses = [
        ('CS101', 'Introduction to Computer Science', 'Fundamentals of programming and computer science', teacher_id, 'Fall 2024', 4),
        ('MATH201', 'Calculus I', 'Differential and integral calculus', teacher_id, 'Fall 2024', 4),
        ('PHY101', 'Physics I', 'Classical mechanics and thermodynamics', teacher_id, 'Fall 2024', 4),
    ]
    
    cursor.executemany('''
        INSERT INTO courses (course_code, course_name, description, teacher_id, semester, credits)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', courses)
    
    # Get course IDs
    course1_id = cursor.execute("SELECT id FROM courses WHERE course_code='CS101'").fetchone()['id']
    course2_id = cursor.execute("SELECT id FROM courses WHERE course_code='MATH201'").fetchone()['id']
    course3_id = cursor.execute("SELECT id FROM courses WHERE course_code='PHY101'").fetchone()['id']
    
    # Insert enrollments
    enrollments = [
        (student1_id, course1_id),
        (student1_id, course2_id),
        (student2_id, course1_id),
        (student2_id, course3_id),
        (student3_id, course1_id),
        (student3_id, course2_id),
        (student3_id, course3_id),
    ]
    
    cursor.executemany('''
        INSERT INTO enrollments (student_id, course_id)
        VALUES (?, ?)
    ''', enrollments)
    
    # Insert sample attendance (last 10 days)
    today = datetime.now()
    for i in range(10):
        date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        
        # Student 1 attendance (good attendance)
        cursor.execute('''
            INSERT INTO attendance (course_id, student_id, date, status)
            VALUES (?, ?, ?, ?)
        ''', (course1_id, student1_id, date, 'present' if i < 8 else 'absent'))
        
        cursor.execute('''
            INSERT INTO attendance (course_id, student_id, date, status)
            VALUES (?, ?, ?, ?)
        ''', (course2_id, student1_id, date, 'present'))
        
        # Student 2 attendance (moderate attendance)
        cursor.execute('''
            INSERT INTO attendance (course_id, student_id, date, status)
            VALUES (?, ?, ?, ?)
        ''', (course1_id, student2_id, date, 'present' if i % 2 == 0 else 'absent'))
        
        # Student 3 attendance (excellent attendance)
        cursor.execute('''
            INSERT INTO attendance (course_id, student_id, date, status)
            VALUES (?, ?, ?, ?)
        ''', (course1_id, student3_id, date, 'present'))
    
    # Link parent to student
    cursor.execute('''
        INSERT INTO parent_student_link (parent_id, student_id, relationship)
        VALUES (?, ?, ?)
    ''', (parent_id, student1_id, 'Father'))
    
    # Insert fee records
    fees = [
        (student1_id, 50000.00, 40000.00, 10000.00, (today + timedelta(days=30)).strftime('%Y-%m-%d'), 'partial'),
        (student2_id, 50000.00, 50000.00, 0.00, today.strftime('%Y-%m-%d'), 'paid'),
        (student3_id, 50000.00, 25000.00, 25000.00, (today + timedelta(days=15)).strftime('%Y-%m-%d'), 'partial'),
    ]
    
    cursor.executemany('''
        INSERT INTO fees (student_id, total_amount, paid_amount, due_amount, due_date, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', fees)
    
    # Insert sample events
    events = [
        ('Mid-term Exams', 'Mid-semester examination period', (today + timedelta(days=15)).strftime('%Y-%m-%d'), '09:00:00', 'Main Campus', 'exam', admin_id),
        ('Annual Sports Day', 'Inter-college sports competition', (today + timedelta(days=30)).strftime('%Y-%m-%d'), '08:00:00', 'Sports Complex', 'sports', admin_id),
        ('Science Fair', 'Annual science project exhibition', (today + timedelta(days=45)).strftime('%Y-%m-%d'), '10:00:00', 'Auditorium', 'academic', admin_id),
    ]
    
    cursor.executemany('''
        INSERT INTO events (title, description, event_date, event_time, location, event_type, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', events)
    
    # Insert sample announcements
    announcements = [
        ('Holiday Notice', 'College will remain closed on 2nd October for Gandhi Jayanti', 'high', 'all', admin_id),
        ('Library Hours Extended', 'Library hours extended till 10 PM during exam week', 'normal', 'students', admin_id),
        ('Parent-Teacher Meeting', 'PTM scheduled for next Saturday at 10 AM', 'high', 'parents', admin_id),
    ]
    
    cursor.executemany('''
        INSERT INTO announcements (title, content, priority, target_audience, created_by)
        VALUES (?, ?, ?, ?, ?)
    ''', announcements)
    
    # Inser