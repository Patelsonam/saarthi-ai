import sqlite3
import os
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

os.makedirs('database', exist_ok=True)
DATABASE_PATH = 'database/saarthi.db'

print("Creating SaarthiAI Database...")

conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

try:
    print("Creating users table...")
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

    print("Creating students table...")
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

    print("Creating courses table...")
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

    print("Creating enrollments table...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            enrollment_date DATE DEFAULT CURRENT_DATE,
            status TEXT DEFAULT 'active',
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (course_id) REFERENCES courses(id),
            UNIQUE(student_id, course_id)
        )
    ''')

    print("Creating attendance table...")
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

    print("Creating parent_student_link table...")
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

    print("Creating fees table...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            total_amount DECIMAL(10, 2) NOT NULL,
            paid_amount DECIMAL(10, 2) DEFAULT 0,
            due_amount DECIMAL(10, 2) NOT NULL,
            due_date DATE,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    ''')

    conn.commit()
    print("All tables created successfully!")

    print("\nInserting sample users...")
    users = [
        ('admin', generate_password_hash('admin123'), 'Admin User', 'admin@saarthi.ai', 'admin'),
        ('teacher1', generate_password_hash('teacher123'), 'Dr. Ravinder Kumar', 'ravinder.kumar@saarthi.ai', 'teacher'),
        ('student1', generate_password_hash('student123'), 'Pinki Dagar', 'pinkidagar@12110202@gmail.com', 'student'),
        ('parent1', generate_password_hash('parent123'), 'Rajesh Kumar', 'rajesh.kumar@parent.saarthi.ai', 'parent'),
    ]

    for user in users:
        try:
            cursor.execute('''INSERT INTO users (username, password, full_name, email, role) VALUES (?, ?, ?, ?, ?)''', user)
            print(f"Created user: {user[0]}")
        except sqlite3.IntegrityError:
            print(f"User already exists: {user[0]}")

    conn.commit()

    cursor.execute("SELECT id FROM users WHERE username='teacher1'")
    teacher_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT id FROM users WHERE username='student1'")
    student_user_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT id FROM users WHERE username='parent1'")
    parent_id = cursor.fetchone()[0]

    print("\nInserting sample student...")
    try:
        cursor.execute('''INSERT INTO students (user_id, student_id, first_name, last_name, email, phone, date_of_birth, gender, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (student_user_id, '2024001', 'Aarav', 'Singh', 'aarav.singh@student.saarthi.ai', '9876543210', '2006-05-15', 'Male', 'Mumbai, Maharashtra'))
        print("Created student: Aarav Singh")
    except sqlite3.IntegrityError:
        print("Student already exists")

    conn.commit()

    cursor.execute("SELECT id FROM students WHERE student_id='2024001'")
    student_db_id = cursor.fetchone()[0]

    print("\nInserting sample course...")
    try:
        cursor.execute('''INSERT INTO courses (course_code, course_name, description, teacher_id, semester, credits) VALUES (?, ?, ?, ?, ?, ?)''', ('CS101', 'Introduction to Computer Science', 'Fundamentals of programming', teacher_id, 'Fall 2024', 4))
        print("Created course: CS101")
    except sqlite3.IntegrityError:
        print("Course already exists")

    conn.commit()

    cursor.execute("SELECT id FROM courses WHERE course_code='CS101'")
    course_id = cursor.fetchone()[0]

    print("\nEnrolling student in course...")
    try:
        cursor.execute('''INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)''', (student_db_id, course_id))
        print("Enrolled student in CS101")
    except sqlite3.IntegrityError:
        print("Enrollment already exists")

    conn.commit()

    print("\nAdding sample attendance...")
    today = datetime.now()
    for i in range(10):
        date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        status = 'present' if i < 8 else 'absent'
        try:
            cursor.execute('''INSERT INTO attendance (course_id, student_id, date, status) VALUES (?, ?, ?, ?)''', (course_id, student_db_id, date, status))
        except sqlite3.IntegrityError:
            pass

    print("Added 10 attendance records")
    conn.commit()

    print("\nLinking parent to student...")
    try:
        cursor.execute('''INSERT INTO parent_student_link (parent_id, student_id, relationship) VALUES (?, ?, ?)''', (parent_id, student_db_id, 'Father'))
        print("Linked parent to student")
    except sqlite3.IntegrityError:
        print("Link already exists")

    conn.commit()

    print("\nAdding fee record...")
    try:
        cursor.execute('''INSERT INTO fees (student_id, total_amount, paid_amount, due_amount, due_date, status) VALUES (?, ?, ?, ?, ?, ?)''', (student_db_id, 50000.00, 40000.00, 10000.00, (today + timedelta(days=30)).strftime('%Y-%m-%d'), 'partial'))
        print("Added fee record")
    except sqlite3.IntegrityError:
        print("Fee record already exists")

    conn.commit()

    print("\n" + "="*50)
    print("DATABASE INITIALIZED SUCCESSFULLY!")
    print("="*50)
    print("\nDefault Login Credentials:")
    print("Admin:   admin / admin123")
    print("Teacher: teacher1 / teacher123")
    print("Student: student1 / student123")
    print("Parent:  parent1 / parent123")
    print("="*50)

except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()

finally:
    conn.close()

print("\nDatabase file created at: database/saarthi.db")