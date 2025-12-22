"""
SaarthiAI Setup Script
Automatically sets up the project environment
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def create_directories():
    """Create necessary directories"""
    directories = [
        'database',
        'face_recognition/models',
        'face_recognition/utils',
        'ai_assistant',
        'config',
        'static/css',
        'static/js',
        'static/images',
        'static/uploads',
        'templates/admin',
        'templates/teacher',
        'templates/student',
        'templates/parent',
        'templates/errors'
    ]
    
    print("\n📁 Creating directories...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   ✅ {directory}")
    
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    print("   This may take 5-10 minutes...")
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("   ✅ All dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ⚠️  Some packages failed to install: {e}")
        print("   You can continue - the system will work with available packages")
        return True

def initialize_database():
    """Initialize the database"""
    print("\n🗄️  Initializing database...")
    try:
        from database.db_utils import init_db
        init_db()
        print("   ✅ Database initialized with sample data!")
        return True
    except Exception as e:
        print(f"   ❌ Database initialization failed: {e}")
        return False

def create_env_file():
    """Create .env file from example"""
    print("\n⚙️  Creating environment configuration...")
    
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as src:
                content = src.read()
            with open('.env', 'w') as dst:
                dst.write(content)
            print("   ✅ .env file created!")
            print("   ⚠️  Please add your GEMINI_API_KEY to .env file")
        else:
            # Create a basic .env file
            with open('.env', 'w') as f:
                f.write("# SaarthiAI Environment Configuration\n")
                f.write("# Get your API key from: https://makersuite.google.com/app/apikey\n\n")
                f.write("GEMINI_API_KEY=your_api_key_here\n")
                f.write("FLASK_SECRET_KEY=your_secret_key_here\n")
                f.write("DEBUG=True\n")
            print("   ✅ .env file created!")
    else:
        print("   ℹ️  .env file already exists")
    
    return True

def main():
    """Main setup function"""
    print("=" * 60)
    print("🎓 SaarthiAI - Automatic Setup")
    print("=" * 60)
    
    # Step 1: Check Python version
    if not check_python_version():
        return False
    
    # Step 2: Create directories
    if not create_directories():
        return False
    
    # Step 3: Install dependencies
    print("\n⚠️  The next step will install Python packages.")
    response = input("   Continue? (y/n): ").lower()
    if response == 'y':
        install_dependencies()
    else:
        print("   ⏭️  Skipping package installation")
    
    # Step 4: Initialize database
    try:
        if not initialize_database():
            print("   ⚠️  You can initialize the database later by running:")
            print("      python database/db_utils.py")
    except ImportError:
        print("   ℹ️  Database will be initialized on first run")
    
    # Step 5: Create .env file
    create_env_file()
    
    # Final instructions
    print("\n" + "=" * 60)
    print("✅ Setup Complete!")
    print("=" * 60)
    print("\n📝 Next Steps:")
    print("   1. Edit .env file and add your GEMINI_API_KEY")
    print("   2. Get API key from: https://makersuite.google.com/app/apikey")
    print("   3. Run: python app.py")
    print("   4. Open browser: http://localhost:5000")
    print("\n🔑 Default Login Credentials:")
    print("   Admin:   admin / admin123")
    print("   Teacher: teacher1 / teacher123")
    print("   Student: student1 / student123")
    print("   Parent:  parent1 / parent123")
    print("=" * 60)
    
    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)