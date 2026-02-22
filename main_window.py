"""Main window — Arabic RTL, modern card UI, company logo in top bar."""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from lang import C, F, T
from employee_form import EmployeeForm
from employee_detail import EmployeeDetail
from settings_window import SettingsWindow

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class MainWindow:
    def __init__(self, root, db, logo_path=None):
        self.root = root
        self.db = db
        self._logo_ref = None

        self.root.title(T["app_title"])
        self.root.geometry("1150x700")
        self.root.minsize(900, 580)
        self.root.configure(bg=C["bg"])
        self._center()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._apply_styles()
        self._build_ui(logo_path)
        self.refresh_list()

    def _center(self):
        self.root.update_idletasks()
        w, h = 1150, 700
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _apply_styles(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("Treeview",
                    background=C["white"], foreground=C["text"],
                    fieldbackground=C["white"], rowheight=42,
                    font=F["body"], borderwidth=0)
        s.configure("Treeview.Heading",
                    background=C["topbar"], foreground="white",
                    font=F["h3"], relief="flat", padding=(8, 10))
        s.map("Treeview",
              background=[("selected", C["selected"])],
              foreground=[("selected", "white")])
        s.map("Treeview.Heading",
              background=[("active", C["topbar2"])])

    def _build_ui(self, logo_path):
        # ── TOP BAR ───────────────────────────────────────────────────────────
        topbar = tk.Frame(self.root, bg=C["topbar"], height=62)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        # Left side: action buttons
        left = tk.Frame(topbar, bg=C["topbar"])
        left.pack(side="left", padx=12)
        self._tbtn(left, T["settings"],    self._open_settings).pack(side="left", padx=3)
        self._tbtn(left, T["backup"],      self._backup).pack(side="left", padx=3)
        self._tbtn(left, T["add_employee"],self._add_employee,
                   bg=C["accent"], hover=C["accent_hover"]).pack(side="left", padx=3)

        # Right side: logo + app title
        right = tk.Frame(topbar, bg=C["topbar"])
        right.pack(side="right", padx=16)

        # ✅ LOGO LINE 3 — company logo in the top-right corner of the main window
        # Displayed at 44x44 px next to the app title.
        # Replace company_logo.png with your image file.
        if logo_path and os.path.exists(logo_path) and PIL_AVAILABLE:
            try:
                img = Image.open(logo_path).convert("RGBA")
                img.thumbnail((44, 44), Image.LANCZOS)
                self._logo_ref = ImageTk.PhotoImage(img)
                tk.Label(right, image=self._logo_ref,
                         bg=C["topbar"]).pack(side="right", padx=(6, 0))
            except Exception:
                pass

        tk.Label(right, text=T["app_title"], font=F["h1"],
                 bg=C["topbar"], fg="white").pack(side="right")

        # ── CONTENT ───────────────────────────────────────────────────────────
        content = tk.Frame(self.root, bg=C["bg"])
        content.pack(fill="both", expand=True, padx=18, pady=16)

        # Search card
        search_card = tk.Frame(content, bg=C["white"],
                               highlightthickness=1,
                               highlightbackground=C["border"])
        search_card.pack(fill="x", pady=(0, 14))
        inner_s = tk.Frame(search_card, bg=C["white"])
        inner_s.pack(fill="x", padx=14, pady=10)

        tk.Button(inner_s, text=T["clear"],
                  command=lambda: self.search_var.set(""),
                  bd=0, bg=C["white"], fg=C["subtext"],
                  font=F["body"], cursor="hand2").pack(side="left", padx=4)

        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *a: self.refresh_list())
        tk.Entry(inner_s, textvariable=self.search_var,
                 font=F["body"], bd=0, bg=C["white"],
                 fg=C["text"], insertbackground=C["text"],
                 justify="right").pack(side="right", fill="x", expand=True)
        tk.Label(inner_s, text=f"🔍  {T['search_hint']}",
                 font=F["small"], bg=C["white"],
                 fg=C["subtext"]).pack(side="right", padx=8)

        # Table card
        tcard = tk.Frame(content, bg=C["white"],
                         highlightthickness=1, highlightbackground=C["border"])
        tcard.pack(fill="both", expand=True)

        cols = ("employee_id", "name", "department", "job_title", "phone")
        self.tree = ttk.Treeview(tcard, columns=cols, show="headings",
                                  selectmode="browse")
        for col, text, w in [
            ("employee_id", T["emp_id"],    130),
            ("name",        T["full_name"], 210),
            ("department",  T["department"],170),
            ("job_title",   T["job_title"], 190),
            ("phone",       T["phone"],     140),
        ]:
            self.tree.heading(col, text=text, anchor="e")
            self.tree.column(col, width=w, minwidth=90, anchor="e")

        vsb = ttk.Scrollbar(tcard, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", self._open_employee)
        self.tree.bind("<Return>",   self._open_employee)
        self.tree.tag_configure("alt", background=C["row_alt"])

        # Right-click menu
        ctx = tk.Menu(self.root, tearoff=0, font=F["body"])
        ctx.add_command(label=T["view_edit"],  command=self._open_selected)
        ctx.add_separator()
        ctx.add_command(label=T["delete_emp"], command=self._delete_selected)
        self.tree.bind("<Button-3>", lambda e: (
            self.tree.selection_set(self.tree.identify_row(e.y)),
            self.tree.focus(self.tree.identify_row(e.y)),
            ctx.post(e.x_root, e.y_root)
        ))

        # Status bar
        sbar = tk.Frame(self.root, bg=C["section_bg"], height=30)
        sbar.pack(fill="x", side="bottom")
        sbar.pack_propagate(False)
        self.status_var = tk.StringVar(value=T["ready"])
        tk.Label(sbar, textvariable=self.status_var,
                 font=F["small"], bg=C["section_bg"],
                 fg=C["subtext"]).pack(side="right", padx=14)

    def _tbtn(self, parent, text, cmd, bg=None, hover=None):
        bg    = bg    or C["topbar2"]
        hover = hover or C["topbar"]
        return tk.Button(parent, text=text, command=cmd,
                         bg=bg, fg="white", font=F["small"],
                         relief="flat", padx=14, pady=7,
                         cursor="hand2", bd=0,
                         activebackground=hover, activeforeground="white")

    def refresh_list(self):
        q = self.search_var.get().strip() if hasattr(self, "search_var") else ""
        emps = self.db.search_employees(q)
        self.tree.delete(*self.tree.get_children())
        for i, emp in enumerate(emps):
            name = f"{emp.get('first_name','') or ''} {emp.get('last_name','') or ''}".strip()
            tag  = "alt" if i % 2 else ""
            self.tree.insert("", "end", iid=emp["employee_id"], tags=(tag,), values=(
                emp["employee_id"], name,
                emp.get("department","") or "",
                emp.get("job_title","")  or "",
                emp.get("phone","")      or "",
            ))
        n = len(emps)
        self.status_var.set(f"{n}  {T['employees_found']}")

    def _add_employee(self):
        EmployeeForm(self.root, self.db, on_save=self.refresh_list)

    def _open_employee(self, event=None):
        sel = self.tree.focus()
        if sel:
            EmployeeDetail(self.root, self.db, sel, on_update=self.refresh_list)

    def _open_selected(self):
        self._open_employee()

    def _delete_selected(self):
        sel = self.tree.focus()
        if not sel:
            return
        emp  = self.db.get_employee(sel)
        name = f"{emp.get('first_name','') or ''} {emp.get('last_name','') or ''}".strip()
        if messagebox.askyesno(T["del_title"],
                               T["del_confirm"].format(name=name),
                               icon="warning"):
            self.db.delete_employee(sel)
            self.refresh_list()
            self.status_var.set(T["deleted"].format(name=name))

    def _backup(self):
        dest = filedialog.askdirectory(title=T["backup_title"])
        if not dest:
            return
        try:
            path = self.db.backup(dest)
            messagebox.showinfo(T["backup_done"], T["backup_ok"].format(path=path))
        except Exception as e:
            messagebox.showerror(T["backup_fail"], str(e))

    def _open_settings(self):
        SettingsWindow(self.root, self.db)

    def _on_close(self):
        self.db.close()
        self.root.destroy()
