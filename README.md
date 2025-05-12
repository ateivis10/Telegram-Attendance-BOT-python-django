✅ Step 1: Project Setup (Django + Bot)
🧰 Requirements
Make sure you have the following installed:
Python 3.8+
pip
Virtual environment (venv)
SQLite

🧱 1.1. Create Project Structure
Open your terminal in VS Code and run:
mkdir telegram_attendance
cd telegram_attendance
python -m venv venv
venv\Scripts\activate

📦 1.2. Install Dependencies
pip install django djangorestframework python-telegram-bot

Then freeze the requirements:
pip freeze > requirements.txt

⚙️ 1.3. Start Django Project
django-admin startproject attendance_project .
python manage.py startapp attendance_app

Add your app and rest_framework to INSTALLED_APPS in attendance_project/settings.py:
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'attendance_app',
]

🧪 1.4. Run Initial Server
python manage.py migrate
python manage.py runserver

Visit http://127.0.0.1:8000/ — You should see the Django welcome page.

✅ Step 2: Setting Up the Telegram Bot

🤖 2.1 Create Your Bot on Telegram
Open Telegram and search for @BotFather

Type /newbot and follow the prompts:
Give it a name (e.g., GUB Attendance Bot)
Set a unique username (must end in bot, e.g., gub_attendance_bot)
BotFather will give you a Bot Token. Copy this (we’ll use it soon).


📦 2.2 Install Telegram Bot Library
In your VS Code terminal (while the virtual environment is active), run:
pip install python-telegram-bot


📝 2.3 Create bot.py File

✅ Step 3: Django Integration — Create Models & Save Attendance
📁 3.1 Define Django Models
🛠️ 3.2 Register Models in admin.py
🔧 3.3 Run Migrations

✅ Step 4: Connect Bot with Django Models
Use Django ORM inside the bot
Automatically create Employee if the user is new
Save check-in and check-out to the Attendance model


