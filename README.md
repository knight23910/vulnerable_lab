# vulnerable_lab
🔐 Vulnerable Lab - A deliberately insecure web application for cybersecurity education, featuring 6 common vulnerabilities (SQL Injection, XSS, Command Injection, IDOR, File Upload, Weak Authentication). Built with Flask and Bootstrap.
# 🔐 Vulnerable Lab

<div align="center">

![Vulnerable Lab Banner](https://img.shields.io/badge/Vulnerable%20Lab-Cybersecurity%20Education-purple?style=for-the-badge&logo=python)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.2-green?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3.x-blue?style=flat-square&logo=sqlite)](https://www.sqlite.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.1.3-purple?style=flat-square&logo=bootstrap)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

**A Deliberately Insecure Web Application for Cybersecurity Education**

[Features](#-features) • [Vulnerabilities](#-vulnerabilities-included) • [Installation](#-installation) • [Usage](#-usage) • [Screenshots](#-screenshots) • [Contributing](#-contributing)

</div>

---

## ⚠️ IMPORTANT DISCLAIMER

> **THIS APPLICATION IS INTENTIONALLY VULNERABLE!**
>
> - **DO NOT** deploy on production or public servers
> - **DO NOT** use for illegal purposes
> - **ONLY** use in controlled, educational environments
> - **ALWAYS** follow ethical guidelines when testing

---

## 📋 Overview

Vulnerable Lab is a **deliberately insecure web application** designed for cybersecurity education and penetration testing practice. It contains multiple common web vulnerabilities for learning purposes, making it an ideal platform for:

- 🎓 **Cybersecurity Students** - Learn about common vulnerabilities
- 🛡️ **Security Professionals** - Practice penetration testing skills
- 👨‍💻 **Software Developers** - Understand secure coding practices
- 🏆 **CTF Players** - Practice exploitation techniques
- 📚 **Security Educators** - Teach web application security

---

## 🚨 Vulnerabilities Included

| # | Vulnerability | Location | Severity | OWASP Category |
|---|---------------|----------|----------|----------------|
| 1 | **SQL Injection** | Login Page | 🔴 Critical | A03:2021-Injection |
| 2 | **Cross-Site Scripting (XSS)** | Search Page | 🟡 High | A03:2021-Injection |
| 3 | **Command Injection** | Ping Tool | 🔴 Critical | A03:2021-Injection |
| 4 | **IDOR** | Profile/Posts | 🟠 Medium | A01:2021-Broken Access Control |
| 5 | **Unrestricted File Upload** | Upload Page | 🔴 Critical | A05:2021-Security Misconfiguration |
| 6 | **Weak Authentication** | Registration | 🟠 Medium | A07:2021-Identification and Authentication Failures |

### Vulnerability Details

#### 1. SQL Injection
```sql
-- Vulnerable Code
query = f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'"
```
#### Cross-Site Scripting (XSS)
```
<!-- Vulnerable Code -->
{{ query|safe }}

<!-- Test Payload -->
<script>alert('XSS')</script>
```
#### Command Injection
```
# Vulnerable Code
subprocess.check_output(full_cmd, shell=True)

# Test Payload
whoami
ipconfig
echo Hacked! & whoami
```
#### IDOR (Insecure Direct Object Reference)
```
# Vulnerable Code - No Authorization Check
user = User.query.filter_by(username=username).first()

# Test
/profile/admin
/post/1
```
#### Unrestricted File Upload
```
# Vulnerable Code - No Validation
file.save(file_path)

# Test
Upload test.php, malicious.html, test.exe
```
#### Weak Authentication
 ```
# Vulnerable Code - No Validation
# No password complexity requirements
# No email validation
```
### 🛠️ Technology Stack
#### Backend
Python 3.8+ - Core programming language

Flask 2.3.2 - Web framework

Flask-SQLAlchemy - ORM for database

Flask-Login - Session management

SQLite - Database

#### Frontend
Bootstrap 5.1.3 - UI framework

HTML5 - Structure

CSS3 - Styling

JavaScript - Interactivity

Font Awesome - Icons

Security (Intentionally Weak)

SHA256 Hashing - Weak password storage

No CSRF Protection - Vulnerability

No Security Headers - Vulnerability

### 📦 Installation
# Check Python version
```
python --version  # Should be 3.8+
```
# Check pip
```
pip --version
```
#### Step-by-Step Setup
1. Clone the Repository
```
git clone https://github.com/yourusername/vulnerable-lab.git
cd vulnerable-lab
```
3. Create Virtual Environment
```
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```
3. Install Dependencies
```
pip install -r requirements.txt
```
5. Set Up Database
```
# The database will be created automatically when you run the app
# Or manually:
python -c "from src.app import app, db; app.app_context().push(); db.create_all()"
```
5. Run the Application
```
python app.py
```
7. Access the Application
```
http://localhost:5000
```
### 🔑 Default Credentials
```
Username	Password	Role
admin	admin123	👑 Administrator
rahul	rahul123	👤 Regular User
alice	alice123	👤 Regular User
bob	bob123	👤 Regular User
charlie	charlie123	👤 Regular User
```
### 🎯 Usage Guide
Step 1: Explore Vulnerabilities
🔓 SQL Injection
```
Go to Login Page

Enter: admin' OR '1'='1 as username

Enter anything as password

You'll be logged in as admin!
```
💀 XSS (Cross-Site Scripting)
```
Go to Search Page

Search for: <script>alert('XSS')</script>

Observe the alert popup!
```
⚡ Command Injection
```
Go to Ping Tool

Enter: whoami (Windows) or id (Linux)

See system command output!
```
🔍 IDOR
```
Go to Profile Page

Try: /profile/admin

View admin's profile data!
```
📁 File Upload
```
Go to Upload Page

Upload any file (try .php or .html)

File is accepted without validation!
```
🔑 Weak Authentication
```
Go to Registration Page

Register with password 123

Email: invalid (no validation!)
```
## 📁 Project Structure
```
├── app.py              # Main application with all vulnerabilities
├── database.py       # Database models
├── README.md
├──📄 .gitignore               # Git ignore rules
├── 📄 LICENSE 
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── index.html      # Home page
│   ├── login.html      # SQL Injection vulnerability
│   ├── register.html   # Weak Authentication
│   ├── dashboard.html  # Main dashboard
│   ├── profile.html    # IDOR vulnerability
│   ├── search.html     # XSS vulnerability
│   ├── ping.html       # Command Injection
│   ├── upload.html     # File Upload
│   ├── admin.html      # Admin panel
│   └── post.html       # IDOR vulnerability
├── static/             # CSS/JS files
│   ├── css/style.css
│   └── js/script.js
├── uploads/            # Uploaded files directory
└── instance/           # SQLite database
```

### 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

⚠️ Note: This software contains intentional vulnerabilities and is for educational purposes only.

### ⚠️ Security Notice
NEVER DEPLOY THIS APPLICATION ON A PUBLIC SERVER!

This application is intentionally vulnerable and should only be used:

✅ In a controlled, isolated environment

✅ For educational purposes

✅ For penetration testing practice

✅ For security research

DO NOT USE:

❌ On production systems

❌ On public servers

❌ For illegal activities

❌ With real user data
