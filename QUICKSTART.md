# ⚡ SaarthiAI - Quick Start Guide

Get up and running in 5 minutes!

##  Step-by-Step Instructions

### Step 1: Check Python Installation
```bash
python --version
```
You need Python 3.8 or higher.

### Step 2: Navigate to Project
```bash
cd saarthi-ai
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database
```bash
python database/db_utils.py
```

### Step 5: Configure API Key (Optional for AI)
```bash
# Edit .env file
GEMINI_API_KEY=your_key_here
```
Get key from: https://makersuite.google.com/app/apikey

### Step 6: Run Application
```bash
python app.py
```

### Step 7: Open Browser
```
http://localhost:5000
```

### Step 8: Login
Try any of these:
- Admin: `admin` / `admin123`
- Teacher: `teacher1` / `teacher123`
- Student: `student1` / `student123`
- Parent: `parent1` / `parent123`

##  You're Done!

Start exploring the features:
- ✅ Face recognition attendance
- ✅ AI learning assistant
- ✅ Real-time dashboards
- ✅ Parent monitoring

##  Tips

1. **For Face Recognition**: Allow camera access when prompted
2. **For AI Features**: Configure Gemini API key in .env
3. **For Best Performance**: Use latest Chrome/Firefox browser

##  Need Help?

- Can't install packages? Try: `pip install --upgrade pip`
- Port 5000 busy? Edit app.py and change port to 8080
- Camera not working? Check browser permissions

Happy Learning! 