"""
Database module - handles all SQLite operations with encryption.
Data is stored in C:/ProgramData/PersonnelSystem (Windows) so the app
works correctly when installed via the installer into Program Files.
"""

import sqlite3
import os
import hashlib
import shutil
import sys
from datetime import datetime
from cryptography.fernet import Fernet


def get_data_dir():
    """
    Return the writable data directory for the app.
    - On Windows (installed): C:\\ProgramData\\PersonnelSystem
    - On Windows (running from source/dev): folder next to main.py
    - On other OS: ~/.PersonnelSystem
    """
    if sys.platform == "win32":
        # ProgramData is always writable by all users
        base = os.environ.get("PROGRAMDATA", "C:\\ProgramData")
        data_dir = os.path.join(base, "PersonnelSystem")
    else:
        data_dir = os.path.join(os.path.expanduser("~"), ".PersonnelSystem")

    os.makedirs(data_dir, exist_ok=True)
    return data_dir


# All file paths are inside the writable data directory
DATA_DIR  = get_data_dir()
DB_FILE   = os.path.join(DATA_DIR, "personnel.db")
KEY_FILE  = os.path.join(DATA_DIR, "personnel.key")
FILES_DIR = os.path.join(DATA_DIR, "employee_files")


def get_or_create_key():
    """Load existing encryption key or create a new one."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key


class Database:
    def __init__(self):
        os.makedirs(FILES_DIR, exist_ok=True)
        self.key    = get_or_create_key()
        self.fernet = Fernet(self.key)
        self.conn   = sqlite3.connect(DB_FILE)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
        self._create_default_admin()

    def _create_tables(self):
        c = self.conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id TEXT UNIQUE NOT NULL,
                first_name TEXT, last_name TEXT,
                date_of_birth TEXT, gender TEXT,
                nationality TEXT, national_id TEXT,
                passport_number TEXT, marital_status TEXT,
                phone TEXT, email TEXT, address TEXT,
                emergency_contact_name TEXT, emergency_contact_phone TEXT,
                department TEXT, job_title TEXT,
                hire_date TEXT, employment_type TEXT,
                salary TEXT, manager TEXT, work_location TEXT,
                spouse_name TEXT, children_count TEXT, family_notes TEXT,
                notes TEXT, photo_path TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id TEXT NOT NULL,
                doc_name TEXT NOT NULL,
                doc_type TEXT,
                file_path TEXT NOT NULL,
                uploaded_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
            )
        """)
        self.conn.commit()

    def _create_default_admin(self):
        c = self.conn.cursor()
        c.execute("SELECT COUNT(*) FROM users")
        if c.fetchone()[0] == 0:
            self.add_user("admin", "admin123")

    def _hash(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # ── Users ─────────────────────────────────────────────────────────────────

    def verify_login(self, username, password):
        c = self.conn.cursor()
        c.execute("SELECT password_hash FROM users WHERE username=?", (username,))
        row = c.fetchone()
        return bool(row and row["password_hash"] == self._hash(password))

    def add_user(self, username, password):
        try:
            c = self.conn.cursor()
            c.execute("INSERT INTO users (username, password_hash) VALUES (?,?)",
                      (username, self._hash(password)))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_users(self):
        c = self.conn.cursor()
        c.execute("SELECT id, username, created_at FROM users")
        return [dict(r) for r in c.fetchall()]

    def delete_user(self, user_id):
        c = self.conn.cursor()
        c.execute("DELETE FROM users WHERE id=?", (user_id,))
        self.conn.commit()

    def change_password(self, username, new_password):
        c = self.conn.cursor()
        c.execute("UPDATE users SET password_hash=? WHERE username=?",
                  (self._hash(new_password), username))
        self.conn.commit()

    # ── Employees ─────────────────────────────────────────────────────────────

    def add_employee(self, data: dict):
        c = self.conn.cursor()
        fields = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        c.execute(f"INSERT INTO employees ({fields}) VALUES ({placeholders})",
                  list(data.values()))
        self.conn.commit()

    def update_employee(self, employee_id, data: dict):
        data["updated_at"] = datetime.now().isoformat()
        c = self.conn.cursor()
        set_clause = ", ".join([f"{k}=?" for k in data.keys()])
        c.execute(f"UPDATE employees SET {set_clause} WHERE employee_id=?",
                  list(data.values()) + [employee_id])
        self.conn.commit()

    def get_employee(self, employee_id):
        c = self.conn.cursor()
        c.execute("SELECT * FROM employees WHERE employee_id=?", (employee_id,))
        row = c.fetchone()
        return dict(row) if row else None

    def search_employees(self, query=""):
        c = self.conn.cursor()
        if query:
            q = f"%{query}%"
            c.execute("""
                SELECT employee_id, first_name, last_name,
                       department, job_title, phone, photo_path
                FROM employees
                WHERE employee_id LIKE ? OR first_name LIKE ?
                   OR last_name LIKE ? OR department LIKE ?
                   OR job_title LIKE ?
                ORDER BY last_name, first_name
            """, (q, q, q, q, q))
        else:
            c.execute("""
                SELECT employee_id, first_name, last_name,
                       department, job_title, phone, photo_path
                FROM employees ORDER BY last_name, first_name
            """)
        return [dict(r) for r in c.fetchall()]

    def delete_employee(self, employee_id):
        c = self.conn.cursor()
        c.execute("SELECT file_path FROM documents WHERE employee_id=?", (employee_id,))
        for doc in c.fetchall():
            try:
                if os.path.exists(doc["file_path"]):
                    os.remove(doc["file_path"])
            except Exception:
                pass
        folder = self._emp_folder(employee_id)
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)
        c.execute("DELETE FROM documents WHERE employee_id=?", (employee_id,))
        c.execute("DELETE FROM employees WHERE employee_id=?", (employee_id,))
        self.conn.commit()

    def get_all_departments(self):
        c = self.conn.cursor()
        c.execute("""SELECT DISTINCT department FROM employees
                     WHERE department IS NOT NULL AND department != ''
                     ORDER BY department""")
        return [r[0] for r in c.fetchall()]

    # ── Documents ─────────────────────────────────────────────────────────────

    def _emp_folder(self, employee_id):
        folder = os.path.join(FILES_DIR, employee_id)
        os.makedirs(folder, exist_ok=True)
        return folder

    def add_document(self, employee_id, source_path, doc_name, doc_type):
        folder = self._emp_folder(employee_id)
        ext = os.path.splitext(source_path)[1]
        ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = os.path.join(folder, f"{doc_type}_{ts}{ext}")
        shutil.copy2(source_path, dest)
        c = self.conn.cursor()
        c.execute("""INSERT INTO documents
                     (employee_id, doc_name, doc_type, file_path)
                     VALUES (?,?,?,?)""",
                  (employee_id, doc_name, doc_type, dest))
        self.conn.commit()
        return dest

    def get_documents(self, employee_id):
        c = self.conn.cursor()
        c.execute("""SELECT * FROM documents WHERE employee_id=?
                     ORDER BY uploaded_at DESC""", (employee_id,))
        return [dict(r) for r in c.fetchall()]

    def delete_document(self, doc_id):
        c = self.conn.cursor()
        c.execute("SELECT file_path FROM documents WHERE id=?", (doc_id,))
        row = c.fetchone()
        if row:
            try:
                if os.path.exists(row["file_path"]):
                    os.remove(row["file_path"])
            except Exception:
                pass
        c.execute("DELETE FROM documents WHERE id=?", (doc_id,))
        self.conn.commit()

    def set_employee_photo(self, employee_id, source_path):
        folder = self._emp_folder(employee_id)
        ext  = os.path.splitext(source_path)[1].lower()
        dest = os.path.join(folder, f"photo{ext}")
        shutil.copy2(source_path, dest)
        c = self.conn.cursor()
        c.execute("UPDATE employees SET photo_path=? WHERE employee_id=?",
                  (dest, employee_id))
        self.conn.commit()
        return dest

    # ── Backup ────────────────────────────────────────────────────────────────

    def backup(self, dest_folder):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(dest_folder, f"PersonnelBackup_{ts}")
        os.makedirs(backup_dir, exist_ok=True)

        shutil.copy2(DB_FILE,  os.path.join(backup_dir, "personnel.db"))
        shutil.copy2(KEY_FILE, os.path.join(backup_dir, "personnel.key"))
        if os.path.exists(FILES_DIR):
            shutil.copytree(FILES_DIR,
                            os.path.join(backup_dir, "employee_files"))
        return backup_dir

    def close(self):
        self.conn.close()
