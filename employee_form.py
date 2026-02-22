"""Employee add/edit form — Arabic RTL, modern UI."""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os, uuid
from datetime import datetime
from lang import C, F, T

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


# ── Helpers ───────────────────────────────────────────────────────────────────

def field(parent, label_text, row, col, colspan=1, wide=False):
    """Label + styled Entry. Returns StringVar."""
    tk.Label(parent, text=label_text, font=F["small"],
             bg=C["white"], fg=C["subtext"], anchor="e"
             ).grid(row=row, column=col, columnspan=colspan,
                    sticky="e", pady=(8, 1), padx=(4, 8))
    var = tk.StringVar()
    frame = tk.Frame(parent, bg=C["input_border"], padx=1, pady=1)
    frame.grid(row=row+1, column=col, columnspan=colspan,
               sticky="ew", pady=(0, 4), padx=(4, 8))
    tk.Entry(frame, textvariable=var, font=F["body"],
             bd=0, bg=C["input_bg"], fg=C["text"],
             insertbackground=C["text"], justify="right"
             ).pack(fill="x", padx=4, pady=4)
    return var


def combo(parent, label_text, row, col, values, colspan=1):
    """Label + styled Combobox. Returns StringVar."""
    tk.Label(parent, text=label_text, font=F["small"],
             bg=C["white"], fg=C["subtext"], anchor="e"
             ).grid(row=row, column=col, columnspan=colspan,
                    sticky="e", pady=(8, 1), padx=(4, 8))
    var = tk.StringVar()
    cb = ttk.Combobox(parent, textvariable=var, values=values,
                      font=F["body"], state="readonly", justify="right")
    cb.grid(row=row+1, column=col, columnspan=colspan,
            sticky="ew", pady=(0, 4), padx=(4, 8))
    return var


def section(parent, text, row, cols=4):
    """Coloured section divider row."""
    fr = tk.Frame(parent, bg=C["section_bg"])
    fr.grid(row=row, column=0, columnspan=cols, sticky="ew",
            pady=(16, 6), padx=0)
    tk.Label(fr, text=f"  {text}  ", font=F["h3"],
             bg=C["section_bg"], fg=C["section_fg"]
             ).pack(side="right", pady=5)


# ── Form class ────────────────────────────────────────────────────────────────

class EmployeeForm:
    def __init__(self, parent, db, employee_id=None, on_save=None):
        self.parent     = parent
        self.db         = db
        self.employee_id = employee_id
        self.on_save    = on_save
        self.photo_path = None
        self._photo_image = None

        self.window = tk.Toplevel(parent)
        self.window.title(T["edit_emp_title"] if employee_id else T["add_emp_title"])
        self.window.geometry("820x720")
        self.window.resizable(True, True)
        self.window.configure(bg=C["bg"])
        self._center()
        self._build_ui()

        if employee_id:
            self._load(employee_id)

        self.window.grab_set()
        self.window.focus_force()

    def _center(self):
        self.window.update_idletasks()
        w, h = 820, 720
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _build_ui(self):
        # Header bar
        hdr = tk.Frame(self.window, bg=C["topbar"], height=54)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        title = T["edit_emp_title"] if self.employee_id else T["add_emp_title"]
        tk.Label(hdr, text=f"  {title}", font=F["h2"],
                 bg=C["topbar"], fg="white").pack(side="right", padx=16)

        # Scrollable canvas
        outer = tk.Frame(self.window, bg=C["bg"])
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer, bg=C["bg"], highlightthickness=0)
        vsb = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        self.sf = tk.Frame(canvas, bg=C["white"])
        self.sf.bind("<Configure>",
                     lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.sf, anchor="nw")
        canvas.configure(yscrollcommand=vsb.set)
        canvas.bind("<MouseWheel>",
                    lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))
        vsb.pack(side="left", fill="y")
        canvas.pack(side="right", fill="both", expand=True)

        self._build_form(self.sf)

        # Footer buttons
        footer = tk.Frame(self.window, bg=C["white"],
                          highlightthickness=1, highlightbackground=C["border"])
        footer.pack(fill="x")
        inner_f = tk.Frame(footer, bg=C["white"])
        inner_f.pack(padx=16, pady=10, anchor="w")
        tk.Button(inner_f, text=T["btn_save"], command=self._save,
                  bg=C["accent"], fg="white", font=F["h3"],
                  relief="flat", padx=22, pady=8, cursor="hand2",
                  activebackground=C["accent_hover"],
                  activeforeground="white").pack(side="left", padx=(0, 8))
        tk.Button(inner_f, text=T["btn_cancel"], command=self.window.destroy,
                  bg=C["section_bg"], fg=C["text"], font=F["body"],
                  relief="flat", padx=16, pady=8, cursor="hand2").pack(side="left")

    def _build_form(self, f):
        for i in range(4):
            f.columnconfigure(i, weight=1)

        pad = tk.Frame(f, bg=C["white"])
        pad.pack(fill="both", expand=True, padx=16, pady=8)
        for i in range(4):
            pad.columnconfigure(i, weight=1)
        g = pad  # alias

        # ── Photo widget (top-left, RTL so visually top-right) ────────────────
        photo_frame = tk.Frame(g, bg=C["white"])
        photo_frame.grid(row=1, column=0, rowspan=8, sticky="n", padx=8, pady=8)

        self.photo_canvas = tk.Canvas(photo_frame, width=115, height=115,
                                      bg=C["accent_light"],
                                      highlightthickness=2,
                                      highlightbackground=C["border"])
        self.photo_canvas.pack()
        self.photo_canvas.create_text(57, 57, text=T["no_photo"],
                                      fill=C["subtext"], font=F["small"],
                                      tags="ph")
        tk.Button(photo_frame, text=T["btn_set_photo"],
                  command=self._set_photo,
                  bg=C["accent"], fg="white", font=F["tiny"],
                  relief="flat", pady=5, cursor="hand2",
                  activebackground=C["accent_hover"],
                  activeforeground="white").pack(fill="x", pady=(6, 0))

        # ── Section: Basic ────────────────────────────────────────────────────
        section(g, T["sec_basic"], 0, 4)

        self.eid_var = field(g, T["f_emp_id"],     1, 3)
        self.fn_var  = field(g, T["f_first_name"], 1, 2)
        self.ln_var  = field(g, T["f_last_name"],  1, 1)

        # Pre-fill employee ID
        self.eid_var.set(self._gen_id())

        self.dob_var    = field(g, T["f_dob"],         3, 3)
        self.gender_var = combo(g, T["f_gender"],      3, 2, T["genders"])
        self.nat_var    = field(g, T["f_nationality"], 3, 1)

        self.natid_var    = field(g, T["f_national_id"], 5, 3)
        self.passport_var = field(g, T["f_passport"],    5, 2)
        self.marital_var  = combo(g, T["f_marital"],     5, 1, T["maritals"])

        # ── Section: Contact ──────────────────────────────────────────────────
        section(g, T["sec_contact"], 7, 4)

        self.phone_var = field(g, T["f_phone"], 8, 3)
        self.email_var = field(g, T["f_email"], 8, 2)

        # Full-width address
        tk.Label(g, text=T["f_address"], font=F["small"],
                 bg=C["white"], fg=C["subtext"], anchor="e"
                 ).grid(row=10, column=0, columnspan=4, sticky="e", pady=(8,1), padx=(4,8))
        self.addr_var = tk.StringVar()
        addr_f = tk.Frame(g, bg=C["input_border"], padx=1, pady=1)
        addr_f.grid(row=11, column=0, columnspan=4, sticky="ew", pady=(0,4), padx=(4,8))
        tk.Entry(addr_f, textvariable=self.addr_var, font=F["body"],
                 bd=0, bg=C["input_bg"], fg=C["text"],
                 insertbackground=C["text"], justify="right"
                 ).pack(fill="x", padx=4, pady=4)

        self.ec_name_var  = field(g, T["f_ec_name"],  12, 3)
        self.ec_phone_var = field(g, T["f_ec_phone"], 12, 2)

        # ── Section: Job ──────────────────────────────────────────────────────
        section(g, T["sec_job"], 14, 4)

        self.dept_var     = combo(g, T["f_department"], 15, 3, T["departments"])
        self.title_var    = field(g, T["f_job_title"],  15, 2)
        self.emptype_var  = combo(g, T["f_emp_type"],   15, 1, T["emp_types"])

        self.hire_var     = field(g, T["f_hire_date"], 17, 3)
        self.salary_var   = field(g, T["f_salary"],    17, 2)
        self.manager_var  = field(g, T["f_manager"],   17, 1)
        self.location_var = field(g, T["f_location"],  19, 3)

        # ── Section: Family ───────────────────────────────────────────────────
        section(g, T["sec_family"], 21, 4)

        self.spouse_var   = field(g, T["f_spouse"],   22, 3)
        self.children_var = field(g, T["f_children"], 22, 2)

        tk.Label(g, text=T["f_family_notes"], font=F["small"],
                 bg=C["white"], fg=C["subtext"], anchor="e"
                 ).grid(row=24, column=0, columnspan=4, sticky="e", pady=(8,1), padx=(4,8))
        self.fam_notes = tk.Text(g, height=3, font=F["body"],
                                  relief="solid", bd=1, wrap="word",
                                  bg=C["input_bg"], fg=C["text"])
        self.fam_notes.grid(row=25, column=0, columnspan=4,
                             sticky="ew", pady=(0,4), padx=(4,8))

        # ── Section: Notes ────────────────────────────────────────────────────
        section(g, T["sec_notes"], 26, 4)

        self.notes = tk.Text(g, height=4, font=F["body"],
                              relief="solid", bd=1, wrap="word",
                              bg=C["input_bg"], fg=C["text"])
        self.notes.grid(row=27, column=0, columnspan=4,
                         sticky="ew", pady=(0, 16), padx=(4,8))

    def _gen_id(self):
        return f"EMP-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:4].upper()}"

    def _set_photo(self):
        path = filedialog.askopenfilename(
            title=T["btn_set_photo"],
            filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.gif"),
                       ("All files", "*.*")]
        )
        if path:
            self.photo_path = path
            self._show_photo(path)

    def _show_photo(self, path):
        self.photo_canvas.delete("all")
        if not PIL_AVAILABLE:
            self.photo_canvas.create_text(57, 57, text=T["photo_set"],
                                          fill=C["accent"], font=F["small"])
            return
        try:
            img = Image.open(path)
            img = img.convert("RGB") if img.mode not in ("RGB", "RGBA") else img
            img.thumbnail((115, 115), Image.LANCZOS)
            self._photo_image = ImageTk.PhotoImage(img)
            self.photo_canvas.create_image(57, 57, anchor="center",
                                           image=self._photo_image)
        except Exception:
            self.photo_canvas.create_text(57, 57, text=T["photo_error"],
                                          fill=C["danger"], font=F["small"])

    def _load(self, emp_id):
        emp = self.db.get_employee(emp_id)
        if not emp:
            return
        def s(v): return emp.get(v, "") or ""

        self.eid_var.set(s("employee_id"))
        self.fn_var.set(s("first_name"))
        self.ln_var.set(s("last_name"))
        self.dob_var.set(s("date_of_birth"))
        self.gender_var.set(s("gender"))
        self.nat_var.set(s("nationality"))
        self.natid_var.set(s("national_id"))
        self.passport_var.set(s("passport_number"))
        self.marital_var.set(s("marital_status"))
        self.phone_var.set(s("phone"))
        self.email_var.set(s("email"))
        self.addr_var.set(s("address"))
        self.ec_name_var.set(s("emergency_contact_name"))
        self.ec_phone_var.set(s("emergency_contact_phone"))
        self.dept_var.set(s("department"))
        self.title_var.set(s("job_title"))
        self.emptype_var.set(s("employment_type"))
        self.hire_var.set(s("hire_date"))
        self.salary_var.set(s("salary"))
        self.manager_var.set(s("manager"))
        self.location_var.set(s("work_location"))
        self.spouse_var.set(s("spouse_name"))
        self.children_var.set(s("children_count"))
        self.fam_notes.delete("1.0", "end")
        self.fam_notes.insert("1.0", s("family_notes"))
        self.notes.delete("1.0", "end")
        self.notes.insert("1.0", s("notes"))

        if emp.get("photo_path") and os.path.exists(emp["photo_path"]):
            self._show_photo(emp["photo_path"])

    def _save(self):
        first = self.fn_var.get().strip()
        last  = self.ln_var.get().strip()
        eid   = self.eid_var.get().strip()

        if not first or not last:
            messagebox.showwarning("", T["val_name"], parent=self.window)
            return
        if not eid:
            messagebox.showwarning("", T["val_id"], parent=self.window)
            return

        data = {
            "employee_id":            eid,
            "first_name":             first,
            "last_name":              last,
            "date_of_birth":          self.dob_var.get().strip(),
            "gender":                 self.gender_var.get(),
            "nationality":            self.nat_var.get().strip(),
            "national_id":            self.natid_var.get().strip(),
            "passport_number":        self.passport_var.get().strip(),
            "marital_status":         self.marital_var.get(),
            "phone":                  self.phone_var.get().strip(),
            "email":                  self.email_var.get().strip(),
            "address":                self.addr_var.get().strip(),
            "emergency_contact_name": self.ec_name_var.get().strip(),
            "emergency_contact_phone":self.ec_phone_var.get().strip(),
            "department":             self.dept_var.get(),
            "job_title":              self.title_var.get().strip(),
            "employment_type":        self.emptype_var.get(),
            "hire_date":              self.hire_var.get().strip(),
            "salary":                 self.salary_var.get().strip(),
            "manager":                self.manager_var.get().strip(),
            "work_location":          self.location_var.get().strip(),
            "spouse_name":            self.spouse_var.get().strip(),
            "children_count":         self.children_var.get().strip(),
            "family_notes":           self.fam_notes.get("1.0", "end").strip(),
            "notes":                  self.notes.get("1.0", "end").strip(),
        }

        try:
            if self.employee_id:
                self.db.update_employee(self.employee_id,
                                        {k: v for k, v in data.items()
                                         if k != "employee_id"})
                saved_id = self.employee_id
            else:
                self.db.add_employee(data)
                saved_id = eid

            if self.photo_path:
                self.db.set_employee_photo(saved_id, self.photo_path)

            if self.on_save:
                self.on_save()

            messagebox.showinfo("", T["saved_ok"], parent=self.window)
            self.window.destroy()

        except Exception as e:
            messagebox.showerror("", T["save_err"] + str(e), parent=self.window)
