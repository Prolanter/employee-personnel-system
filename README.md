# Employee Personnel Record System

A secure offline desktop application built with Python (Tkinter) for managing employee personnel records inside a company environment.

## 🔐 Features

* Secure login system
* Add, edit, delete employee records
* Store personal and job information
* Attach scanned documents (passport, ID, contracts)
* Instant search functionality
* Local SQLite database (offline & private)
* Backup system
* Arabic RTL modern interface
* Company logo integration (taskbar + UI)

## 🖥 Technologies Used

* Python 3
* Tkinter (GUI)
* Pillow (Image handling)
* PyInstaller (Executable build)

## 📦 How to Run (Development Mode)

```bash
pip install -r requirements.txt
python main.py
```

## 🏗 Build Executable

```bash
pyinstaller --onefile --windowed --icon=company_logo.ico --add-data "company_logo.png;." main.py
```

## ⚠️ Security Notice

This system is designed for offline internal company usage.
Do not upload or expose the database file publicly.

---

Developed by Mustafa
