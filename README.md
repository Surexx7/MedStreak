# MediScope Platform - Setup Guide

## 📋 Prerequisites

Before you begin, make sure you have the following installed on your computer:

1. **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
2. **VS Code** - [Download VS Code](https://code.visualstudio.com/)
3. **Git** - [Download Git](https://git-scm.com/downloads/)

## 🚀 Step-by-Step Setup Instructions

### Step 1: Download the Project Files

#### Option A: Download ZIP (Easiest)
1. Click the "Download Code" button in v0
2. Extract the ZIP file to your desired location
3. Rename the folder to `mediscope-platform`

#### Option B: Clone from GitHub (If available)
\`\`\`bash
git clone <repository-url>
cd mediscope-platform
\`\`\`

### Step 2: Open in VS Code

1. Open VS Code
2. Click `File` → `Open Folder`
3. Navigate to and select the `mediscope-platform` folder
4. Click `Select Folder`

### Step 3: Install VS Code Extensions (Recommended)

Install these helpful extensions:
1. **Python** (by Microsoft)
2. **Django** (by Baptiste Darthenay)
3. **HTML CSS Support**
4. **SQLite Viewer** (for database inspection)

To install:
1. Press `Ctrl+Shift+X` (Windows/Linux) or `Cmd+Shift+X` (Mac)
2. Search for each extension and click "Install"

### Step 4: Set Up Python Virtual Environment

1. Open VS Code Terminal: `View` → `Terminal` or `Ctrl+`` (backtick)
2. Create virtual environment:

**Windows:**
\`\`\`bash
python -m venv mediscope_env
mediscope_env\Scripts\activate
\`\`\`

**Mac/Linux:**
\`\`\`bash
python3 -m venv mediscope_env
source mediscope_env/bin/activate
\`\`\`

You should see `(mediscope_env)` at the beginning of your terminal prompt.

### Step 5: Install Dependencies

With your virtual environment activated, install the required packages:

\`\`\`bash
pip install -r requirements.txt
\`\`\`

If you get an error, install packages individually:
\`\`\`bash
pip install Django==4.2.7
pip install Pillow==10.1.0
pip install django-crispy-forms==2.0
pip install crispy-bootstrap4==2022.1
\`\`\`

### Step 6: Set Up the Database

Run these commands in the VS Code terminal:

\`\`\`bash
# Create database migrations
python manage.py makemigrations

# Apply migrations to create database tables
python manage.py migrate

# Create sample data (students, cases, achievements)
python scripts/create_student_data.py
\`\`\`

### Step 7: Run the Development Server

Start the Django development server:

\`\`\`bash
python manage.py runserver
\`\`\`

You should see output like:
\`\`\`
System check identified no issues (0 silenced).
January 07, 2025 - 10:30:00
Django version 4.2.7, using settings 'mediscope.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
\`\`\`

### Step 8: Access the Platform

1. Open your web browser
2. Go to: `http://127.0.0.1:8000/` or `http://localhost:8000/`
3. You should see the MediScope homepage!

## 🔑 Login Credentials

### Admin Access (Full Platform Management)
- **Username:** `admin`
- **Password:** `admin123`
- **URL:** `http://localhost:8000/admin/`

### Demo Student Account
- **Username:** `demo_student`
- **Password:** `mediscope123`

### Other Student Accounts
- **Password:** `password123`
- **Usernames:** `sarah_miller`, `alex_kim`, `mike_rodriguez`, `emma_johnson`, `david_chen`, etc.

## 🛠️ VS Code Configuration

### Python Interpreter Setup
1. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
2. Type "Python: Select Interpreter"
3. Choose the interpreter from your virtual environment:
   - Windows: `mediscope_env\Scripts\python.exe`
   - Mac/Linux: `mediscope_env/bin/python`

### Debugging Setup
Create `.vscode/launch.json` for debugging:

\`\`\`json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Django",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": ["runserver"],
            "django": true,
            "justMyCode": true
        }
    ]
}
\`\`\`

## 📁 Project Structure

\`\`\`
mediscope-platform/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── mediscope/               # Main Django project
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── core/                    # Core app (users, profiles)
│   ├── models.py            # User and profile models
│   ├── views.py             # Core views
│   ├── urls.py              # Core URLs
│   └── forms.py             # User forms
├── cases/                   # Medical cases app
│   ├── models.py            # Case models
│   ├── views.py             # Case views
│   └── urls.py              # Case URLs
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── core/                # Core app templates
│   ├── cases/               # Case templates
│   └── registration/        # Auth templates
├── static/                  # Static files (CSS, JS, images)
├── scripts/                 # Utility scripts
│   └── create_student_data.py
└── db.sqlite3              # SQLite database (created after migration)
\`\`\`

## 🎯 Platform Features

### For Students:
- **Dashboard:** Personal progress tracking
- **Medical Cases:** Interactive case simulations
- **Quizzes:** Knowledge assessment
- **3D Anatomy:** Interactive anatomy exploration
- **AI Symptom Checker:** AI-powered diagnostic practice
- **Gamification:** XP, levels, achievements, leaderboards
- **Profile Management:** Academic info and progress

### For Administrators:
- **Django Admin:** Full platform management
- **User Management:** Student accounts and profiles
- **Content Management:** Cases, quizzes, achievements
- **Analytics:** Student progress and engagement

## 🔧 Common Issues & Solutions

### Issue: "Module not found" error
**Solution:** Make sure your virtual environment is activated and dependencies are installed:
\`\`\`bash
# Activate virtual environment first
source mediscope_env/bin/activate  # Mac/Linux
# or
mediscope_env\Scripts\activate     # Windows

# Then install dependencies
pip install -r requirements.txt
\`\`\`

### Issue: Database errors
**Solution:** Reset the database:
\`\`\`bash
# Delete the database file
rm db.sqlite3  # Mac/Linux
del db.sqlite3  # Windows

# Recreate database
python manage.py migrate
python scripts/create_student_data.py
\`\`\`

### Issue: Port already in use
**Solution:** Use a different port:
\`\`\`bash
python manage.py runserver 8001
\`\`\`

### Issue: Static files not loading
**Solution:** Collect static files:
\`\`\`bash
python manage.py collectstatic
\`\`\`

## 🚀 Development Workflow

### Daily Development:
1. Open VS Code
2. Open terminal in VS Code
3. Activate virtual environment:
   \`\`\`bash
   source mediscope_env/bin/activate  # Mac/Linux
   mediscope_env\Scripts\activate     # Windows
   \`\`\`
4. Start development server:
   \`\`\`bash
   python manage.py runserver
   \`\`\`
5. Open browser to `http://localhost:8000`

### Making Changes:
1. Edit files in VS Code
2. Save changes (`Ctrl+S`)
3. Refresh browser to see changes
4. For model changes, run:
   \`\`\`bash
   python manage.py makemigrations
   python manage.py migrate
   \`\`\`

### Stopping the Server:
- Press `Ctrl+C` in the terminal where the server is running

## 📚 Next Steps

1. **Explore the Platform:** Login with demo credentials and explore features
2. **Customize Content:** Add your own medical cases and quizzes
3. **Modify Styling:** Edit CSS in the templates
4. **Add Features:** Extend the platform with new functionality
5. **Deploy:** Consider deploying to a cloud platform for production use

## 🆘 Getting Help

If you encounter issues:
1. Check the terminal for error messages
2. Ensure all dependencies are installed
3. Verify your virtual environment is activated
4. Check that you're using the correct Python version (3.8+)
5. Review the Django documentation: https://docs.djangoproject.com/

## 🎉 Success!

If you can access `http://localhost:8000` and see the MediScope homepage, congratulations! Your medical education platform is now running successfully.

Happy coding! 🚀
\`\`\`

```python file="requirements.txt"
Django==4.2.7
Pillow==10.1.0
django-crispy-forms==2.0
crispy-bootstrap4==2022.1
