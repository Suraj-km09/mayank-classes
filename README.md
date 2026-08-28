# Mayank Classes - Coaching Center Management & Learning Platform (LMS)

A client-ready, production-grade, API-first Coaching Institute Management and Learning Platform built with **Python, Django, Django REST Framework** and an interactive, modern **HTML5, Vanilla CSS3 & Vanilla JavaScript** frontend.

---

## 🌟 Key Platform Modules & Features

### 1. 🌐 Public Institute Website (`/`)
* **Hero Section**: Animated admission alerts, key national metrics, scholarship CTAs.
* **Course Explorer**: Interactive category tabs (*Engineering JEE, Medical NEET, Foundation Class 9-10, Crash Courses*) with instant syllabus curriculum modal preview.
* **Toppers & Results Hall of Fame**: AIR rank cards, exam breakdowns, and success stories.
* **Faculty Showcase**: Senior mentor profiles with qualifications, years of experience, ratings, and student counts.
* **Notice Board**: Live circular ticker with tags for Exams, Workshops, and Holidays.
* **Student Reviews**: Real-world testimonial carousel.
* **Campus & Lab Gallery**: Modern acoustic classrooms, computer CBT labs, and library pods.
* **Admissions Inquiry Form**: Direct lead capture with counselor auto-routing.

### 2. 👨‍🎓 Student Portal (`/student/`)
* **Overview Dashboard**: Real-time attendance rate, video progression percentage, average test scores, and fee balance.
* **Recorded Video LMS**: Hierarchical course curriculum tree (`Course → Subject → Chapter → Video Lesson`) with embedded playback, video completion tracking, and automatic progress saving.
* **Online Tests & CBT Series**: Timed examination engine with question navigation palette, instant submission evaluation, and detailed step-by-step scorecard breakdown.
* **Study Materials**: Comprehensive downloadable lecture notes, formula cheatsheets, and DPP question banks.
* **Attendance Tracking**: Monthly analytics and daily presence logs.
* **Fee Center**: Installment schedule, invoice ledger, and simulated 1-click online fee payments.
* **Digital Certificates**: Official verifiable academic credentials with unique UUIDs.

### 3. 👨‍🏫 Teacher & Faculty Portal (`/teacher/`)
* **Faculty Workspace**: Assigned batches, active student counts, today's schedule.
* **Interactive Roll Call**: 1-click *"Mark All Present"* or individual `P / A / L` toggles with instant database sync.
* **Lesson Publisher**: Publish video lessons directly into the hierarchical LMS syllabus with preview toggles.
* **Study Material Uploader**: Distribute PDFs, notes, and homework problem sheets.
* **Online Test Builder**: Create timed MCQ examinations with customizable marks, negative deductions, and step explanations.
* **Performance Analytics**: View batch score distributions, student marks, and passing rates.
* **Notice Broadcaster**: Send announcements directly to student dashboard feeds.

### 4. 🛡️ Admin Command Center (`/admin-portal/` & `/django-admin/`)
* **Executive Dashboard**: Real-time KPI summaries for total students, faculty, fee collections, pending dues, and attendance rates.
* **Student Directory CRUD**: Register/admit new students, issue roll numbers, and assign academic classes.
* **Faculty Roster**: Manage teachers and specializations.
* **Batch Timetable**: Schedule lecture halls, timings, and capacity limits.
* **Finance Audit**: Filter paid vs overdue invoices.
* **Lead Inquiries**: Manage and convert prospective student inquiries.

### 5. 🏅 Public Certificate Verification (`/verify-certificate/`)
* Anyone can verify official student certificates using their certificate number or verification UUID (e.g. `c90a5a81-6b01-4aca-bd7c-41b781d94242`).

---

## 🔑 Demo Login Accounts

Quick 1-click login switchers are embedded directly on the `/login/` page for instant reviewer testing:

| Role | Username / Email | Password | Access Area |
| :--- | :--- | :--- | :--- |
| **Student** | `student@mayankclasses.com` (or `student`) | `student123` | `/student/` |
| **Teacher** | `teacher@mayankclasses.com` (or `teacher`) | `teacher123` | `/teacher/` |
| **Admin** | `admin@mayankclasses.com` (or `admin`) | `admin123` | `/admin-portal/` & `/django-admin/` |

---

## 🚀 Quickstart & Local Setup

### 1. Clone & Activate Virtual Environment
```bash
# Clone the repository
git clone <your-repo-url>
cd mayank-classes

# Create and activate virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Migrations & Seed Demo Data
```bash
# Apply database schema
python manage.py migrate

# Seed complete realistic demo data (courses, faculty, students, videos, tests, attendances, invoices)
python manage.py seed_demo_data
```

### 4. Run Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## 🧪 Automated Testing
Run the comprehensive Django REST Framework test suite:
```bash
python manage.py test
```

---

## ☁️ Deployment Guide (PythonAnywhere & Production)

The application is engineered out-of-the-box for **PythonAnywhere free tier**, Heroku, Render, and Linux VPS environments with WhiteNoise static serving.

### Step 1: Upload Code to PythonAnywhere
1. Open a Bash console on PythonAnywhere.
2. Clone your repository:
   ```bash
   git clone <your-repo-url>
   cd mayank-classes
   ```

### Step 2: Set Up Virtual Environment & Dependencies
```bash
mkvirtualenv --python=/usr/bin/python3.10 mayank-venv
pip install -r requirements.txt
```

### Step 3: Run Database Migrations & Collect Static Files
```bash
python manage.py migrate
python manage.py seed_demo_data
python manage.py collectstatic --noinput
```

### Step 4: Configure Web Tab on PythonAnywhere
1. Go to the **Web** tab on PythonAnywhere.
2. Set **Source code** directory: `/home/<your-username>/mayank-classes`
3. Set **Virtualenv** directory: `/home/<your-username>/.virtualenvs/mayank-venv`
4. Under **Static files**:
   - URL: `/static/` -> Directory: `/home/<your-username>/mayank-classes/staticfiles`
   - URL: `/media/` -> Directory: `/home/<your-username>/mayank-classes/media`

### Step 5: Configure WSGI File
Click on the **WSGI configuration file** link on PythonAnywhere and replace its contents with:
```python
import os
import sys

path = '/home/<your-username>/mayank-classes'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
Click **Reload** on the Web tab, and your coaching institute platform is live!

---

## 🐘 PostgreSQL Migration (Production Database)
To switch from SQLite to PostgreSQL:
1. In your `.env` file, specify:
   ```env
   DATABASE_URL=postgres://user:password@localhost:5432/mayank_classes_db
   ```
2. Install `psycopg2-binary` and `dj-database-url`.
3. Run `python manage.py migrate` and `python manage.py seed_demo_data`.

---

## 📡 REST API Reference

| Endpoint | Methods | Description |
| :--- | :--- | :--- |
| `/api/auth/login/` | `POST` | Authenticate user, returns DRF Token & user profile |
| `/api/auth/demo-login/` | `POST` | 1-Click prototype login (`role: student/teacher/admin`) |
| `/api/auth/register/` | `POST` | Self-service student registration |
| `/api/courses/` | `GET, POST` | List and filter active courses |
| `/api/courses/{id}/curriculum/` | `GET` | Complete hierarchy: Course → Subjects → Chapters → Lessons |
| `/api/videos/{id}/progress/` | `POST` | Update video watch duration and completed status |
| `/api/study-materials/` | `GET, POST` | Filter and download notes, DPPs, and formula sheets |
| `/api/tests/` | `GET, POST` | List active mock tests and question series |
| `/api/tests/{id}/start/` | `POST` | Start test attempt and load questions |
| `/api/tests/{id}/submit/` | `POST` | Submit answers, auto-evaluate marks, generate scorecard |
| `/api/attendance/` | `GET, POST` | List records or bulk mark batch attendance |
| `/api/fees/` | `GET, POST` | Student fee ledger & invoice management |
| `/api/fees/{id}/pay/` | `POST` | Simulate online installment fee payment |
| `/api/certificates/verify/{code}/`| `GET` | Public validation of digital certificate authenticity |
| `/api/admin/stats/` | `GET` | Executive dashboard KPI metrics |
