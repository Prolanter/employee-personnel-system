"""Login window — Arabic, modern design, with company logo."""

import tkinter as tk
from tkinter import messagebox
import os
from lang import C, F, T

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class LoginWindow:
    def __init__(self, parent, db, logo_path=None):
        self.db = db
        self.authenticated = False
        self._logo_ref = None
        self._icon_ref = None

        self.window = tk.Toplevel(parent)
        self.window.title(T["login_title"])
        self.window.geometry("420x370")
        self.window.resizable(False, False)
        self.window.configure(bg=C["bg"])
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
        self._center()
        self._build_ui(logo_path)

        # Apply taskbar/titlebar icon AFTER window is drawn
        self.window.update_idletasks()
        self._apply_icon(logo_path)

        self.window.grab_set()
        self.window.focus_force()

    def _center(self):
        self.window.update_idletasks()
        w, h = 420, 370
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _apply_icon(self, logo_path):
        """Set the window icon (taskbar + title bar)."""
        if not logo_path:
            return
        # Try .ico first (same folder, replace .png extension)
        ico_path = os.path.join(os.path.dirname(logo_path), "company_logo.ico")
        try:
            if os.path.exists(ico_path):
                self.window.iconbitmap(ico_path)
                return
        except Exception:
            pass
        # Fallback: use PNG via iconphoto
        try:
            if os.path.exists(logo_path) and PIL_AVAILABLE:
                img = Image.open(logo_path).convert("RGBA")
                self._icon_ref = ImageTk.PhotoImage(img)
                self.window.iconphoto(False, self._icon_ref)
        except Exception:
            pass

    def _build_ui(self, logo_path):
        # ── Top colour band ───────────────────────────────────────────────────
        band = tk.Frame(self.window, bg=C["topbar"], height=110)
        band.pack(fill="x")
        band.pack_propagate(False)

        # Company logo shown in the login header band at 72x72 px
        logo_shown = False
        if logo_path and os.path.exists(logo_path) and PIL_AVAILABLE:
            try:
                img = Image.open(logo_path).convert("RGBA")
                img.thumbnail((72, 72), Image.LANCZOS)
                self._logo_ref = ImageTk.PhotoImage(img)
                lbl = tk.Label(band, image=self._logo_ref, bg=C["topbar"])
                lbl.image = self._logo_ref   # extra anchor against GC
                lbl.pack(pady=(14, 2))
                logo_shown = True
            except Exception:
                pass

        if not logo_shown:
            tk.Label(band, text="🏢", font=("Segoe UI", 28),
                     bg=C["topbar"], fg="white").pack(pady=(16, 2))

        tk.Label(band, text=T["app_title"], font=F["h2"],
                 bg=C["topbar"], fg="white").pack()

        # ── White login card ──────────────────────────────────────────────────
        card = tk.Frame(self.window, bg=C["white"],
                        highlightthickness=1, highlightbackground=C["border"])
        card.pack(fill="both", expand=True, padx=30, pady=18)
        inner = tk.Frame(card, bg=C["white"])
        inner.pack(padx=25, pady=16, fill="both", expand=True)

        tk.Label(inner, text=T["login_username"], font=F["small"],
                 bg=C["white"], fg=C["subtext"], anchor="e").pack(fill="x")
        self.username_var = tk.StringVar()
        self._entry(inner, self.username_var).pack(fill="x", pady=(3, 10))

        tk.Label(inner, text=T["login_password"], font=F["small"],
                 bg=C["white"], fg=C["subtext"], anchor="e").pack(fill="x")
        self.password_var = tk.StringVar()
        pw_frame = self._entry(inner, self.password_var, show="●")
        pw_frame.pack(fill="x", pady=(3, 16))
        for child in pw_frame.winfo_children():
            child.bind("<Return>", lambda e: self._login())

        tk.Button(inner, text=T["login_btn"], command=self._login,
                  bg=C["accent"], fg="white", font=F["h3"],
                  relief="flat", pady=9, cursor="hand2",
                  activebackground=C["accent_hover"],
                  activeforeground="white").pack(fill="x")

        tk.Label(inner, text=T["login_hint"], font=F["tiny"],
                 bg=C["white"], fg=C["subtext"]).pack(pady=(8, 0))

    def _entry(self, parent, var, show=""):
        frame = tk.Frame(parent, bg=C["input_border"], padx=1, pady=1)
        tk.Entry(frame, textvariable=var, show=show,
                 font=F["body"], bd=0, bg=C["input_bg"],
                 fg=C["text"], insertbackground=C["text"],
                 justify="right").pack(fill="x", padx=4, pady=5)
        return frame

    def _login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        if not username or not password:
            messagebox.showwarning(T["login_title"], T["login_empty"],
                                   parent=self.window)
            return
        if self.db.verify_login(username, password):
            self.authenticated = True
            self.window.destroy()
        else:
            messagebox.showerror(T["login_title"], T["login_fail"],
                                 parent=self.window)
            self.password_var.set("")

    def _on_close(self):
        self.authenticated = False
        self.window.destroy()
