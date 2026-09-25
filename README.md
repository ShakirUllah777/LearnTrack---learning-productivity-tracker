# LearnTrack 🎓

> **"Track What You Do. Remember What You Learn."**

**LearnTrack** is a personal student productivity and learning-tracking web application built with **Django** and **Bootstrap 5**. It combines a daily task manager, personal knowledge note hub, and a step-by-step learning progress tracker into a unified, responsive dashboard.

---

## ✨ Key Features

- **🔐 User Authentication**: Secure account creation and login via Email & Password.
- **📋 Task Management**: Create, organize, prioritize (Low, Medium, High), and track daily study tasks with due dates and quick completion toggles.
- **📝 Personal Notes Hub**: Document study notes with content previews, tag filtering, and fast keyword search.
- **📚 Learning Journey Tracker**: Break down skills (e.g., *React.js*, *Python*, *Django*) into sequential topics with real-time status tracking (`✓ Completed`, `→ Currently Learning`, `○ Not Started`) and auto-computed progress percentages.
- **📊 Interactive Dashboard**: Student workspace overview displaying active task counters, recent notes, and visual progress bars.
- **🎨 Modern SaaS UI**: Light-themed, clean card-based layout powered by Bootstrap 5 and Bootstrap Icons.

---

## 🛠️ Tech Stack

- **Backend**: Python, Django 5
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5.3, Bootstrap Icons

---

## 🚀 Quick Start Guide

### Prerequisites

Ensure you have Python 3.10+ installed on your system.

### 1. Clone & Setup Project

```bash
git clone https://github.com/your-username/LearnTrack.git
cd LearnTrack
```

### 2. Create & Activate Virtual Environment

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install django
```

### 4. Apply Database Migrations

```bash
python manage.py migrate
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Open your browser and navigate to: `http://127.0.0.1:8000/`

---

## 📁 Project Structure

```text
LearnTrack/
├── accounts/           # User authentication app (login, register, logout)
├── config/             # Django project settings, root URLs, and core views
├── learning/           # Skills and sequential topics tracking app
├── notes/              # Notes management app
├── tasks/              # Task management app
├── static/             # Static CSS and JS assets
├── templates/          # HTML templates
│   ├── accounts/       # Login and signup pages
│   ├── includes/       # Component partials (Navbar)
│   ├── learning/       # Skill overview and topic timeline pages
│   ├── notes/          # Notes grid and editor pages
│   ├── tasks/          # Task board and editor pages
│   ├── base.html       # Main base layout
│   ├── dashboard.html  # Student workspace dashboard
│   └── home.html       # Landing page
├── db.sqlite3          # SQLite database
├── manage.py           # Django management script
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation
```

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

© 2026 **LearnTrack**. Empowering Lifelong Learners.
