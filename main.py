"""
Employee Personnel Record System - Entry point.

LOGO SETUP:
  Place your logo files in the SAME FOLDER as this main.py file.
  Name them EXACTLY:
    company_logo.png  — shown inside the app (login, top bar)
    company_logo.ico  — used for taskbar icon, desktop shortcut, installer
  Convert PNG to ICO free at: https://convertio.co/png-ico/
"""

import tkinter as tk
import sys
import os

from database import Database
from login_window import LoginWindow
from main_window import MainWindow

# ── Logo file names — rename YOUR files to match these exactly ────────────────
LOGO_PNG = "company_logo.png"
LOGO_ICO = "company_logo.ico"


def get_base_dir():
    """
    Returns the folder where the exe lives (compiled mode)
    or where main.py lives (dev mode).
    PyInstaller sets sys.frozen=True and sys.executable = path to the .exe.
    """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def asset(filename):
    """Full absolute path to a file sitting next to the exe / main.py."""
    return os.path.join(get_base_dir(), filename)


def apply_icon_to_all_windows(root):
    """
    Sets the window icon on the ROOT Tk() object.
    Using iconbitmap(default=...) makes it propagate automatically to ALL
    Toplevel windows (login, main, forms, dialogs) — one call does everything.
    """
    ico = asset(LOGO_ICO)
    png = asset(LOGO_PNG)

    # Best: .ico  — Windows understands it natively, covers taskbar + title bar
    if os.path.exists(ico):
        try:
            root.iconbitmap(default=ico)
            return
        except Exception:
            pass

    # Fallback: .png via iconphoto — works when only .png is provided
    if os.path.exists(png):
        try:
            from PIL import Image, ImageTk
            img = Image.open(png).convert("RGBA")
            photos = []
            for size in [(16, 16), (32, 32), (48, 48), (64, 64)]:
                copy = img.copy()
                copy.thumbnail(size, Image.LANCZOS)
                photos.append(ImageTk.PhotoImage(copy))
            root.iconphoto(True, *photos)
            root._icon_refs = photos   # keep reference — prevents garbage collection
        except Exception:
            pass


def main():
    root = tk.Tk()
    root.withdraw()

    # Set icon BEFORE any window appears — propagates to all child windows
    apply_icon_to_all_windows(root)

    db = Database()

    login = LoginWindow(root, db, logo_path=asset(LOGO_PNG))
    root.wait_window(login.window)

    if login.authenticated:
        root.deiconify()
        MainWindow(root, db, logo_path=asset(LOGO_PNG))
        root.mainloop()
    else:
        root.destroy()


if __name__ == "__main__":
    main()
