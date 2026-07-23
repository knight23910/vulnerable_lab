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

-- Test Payload
admin' OR '1'='1
