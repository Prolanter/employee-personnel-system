"""Employee detail view — Arabic RTL, modern UI."""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os, subprocess, platform
from lang import C, F, T
from employee_form import EmployeeForm

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class EmployeeDetail:
    def __init__(self, parent, db, employee_id, on_update=None):
        self.parent      = parent
        self.db          = db
        self.employee_id = employee_id
        self.on_update   = on_update
        self._photo_image = None
        self._docs_map   = {}

        self.window = tk.Toplevel(parent)
        self.window.title(T["tab_info"])
        self.window.geometry("900x680")
        self.window.resizable(True, True)
        self.window.configure(bg=C["bg"])
        self._center()
        self._build_ui()
        self._load()
        self.window.grab_set()

    def _center(self):
        self.window.update_idletasks()
        w, h = 900, 680
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _build_ui(self):
        # Header
        hdr = tk.Frame(self.window, bg=C["topbar"], height=56)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        left_hdr = tk.Frame(hdr, bg=C["topbar"])
        left_hdr.pack(side="left", padx=12)
        tk.Button(left_hdr, text=T["btn_close"], command=self.window.destroy,
                  bg=C["topbar2"], fg="white", font=F["small"],
                  relief="flat", padx=12, pady=6, cursor="hand2").pack(side="left", padx=4)
        tk.Button(left_hdr, text=T["btn_edit"], command=self._edit,
                  bg=C["success"], fg="white", font=F["small"],
                  relief="flat", padx=12, pady=6, cursor="hand2").pack(side="left", padx=4)

        self.name_lbl = tk.Label(hdr, text="", font=F["h1"],
                                  bg=C["topbar"], fg="white")
        self.name_lbl.pack(side="right", padx=20)

        # Notebook
        style = ttk.Style()
        style.configure("TNotebook.Tab", font=F["body"], padding=[14, 6])
        nb = ttk.Notebook(self.window)
        nb.pack(fill="both", expand=True, padx=12, pady=12)

        self.info_tab = tk.Frame(nb, bg=C["white"])
        nb.add(self.info_tab, text=T["tab_info"])

        self.docs_tab = tk.Frame(nb, bg=C["white"])
        nb.add(self.docs_tab, text=T["tab_docs"])

        self._build_info_tab()
        self._build_docs_tab()

    # ── Info tab ──────────────────────────────────────────────────────────────

    def _build_info_tab(self):
        canvas = tk.Canvas(self.info_tab, bg=C["white"], highlightthickness=0)
        vsb = ttk.Scrollbar(self.info_tab, orient="vertical", command=canvas.yview)
        self.info_frame = tk.Frame(canvas, bg=C["white"])
        self.info_frame.bind("<Configure>",
                             lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.info_frame, anchor="nw")
        canvas.configure(yscrollcommand=vsb.set)
        canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))
        vsb.pack(side="left", fill="y")
        canvas.pack(side="right", fill="both", expand=True)

        for i in range(4):
            self.info_frame.columnconfigure(i, weight=1)

        # Photo canvas
        self.photo_canvas = tk.Canvas(self.info_frame, width=130, height=130,
                                       bg=C["accent_light"],
                                       highlightthickness=2,
                                       highlightbackground=C["border"])
        self.photo_canvas.grid(row=2, column=0, rowspan=10,
                                sticky="n", padx=16, pady=16)
        self.photo_canvas.create_text(65, 65, text=T["no_photo"],
                                       fill=C["subtext"], font=F["small"])

    def _sec(self, f, text, row):
        fr = tk.Frame(f, bg=C["section_bg"])
        fr.grid(row=row, column=0, columnspan=4, sticky="ew", pady=(14, 6), padx=0)
        tk.Label(fr, text=f"  {text}  ", font=F["h3"],
                 bg=C["section_bg"], fg=C["section_fg"]).pack(side="right", pady=5)

    def _row(self, f, label, value, row, col):
        tk.Label(f, text=label, font=F["tiny"], bg=C["white"],
                 fg=C["subtext"], anchor="e").grid(row=row, column=col,
                                                    sticky="e", padx=(4, 8), pady=(6, 0))
        tk.Label(f, text=value or "—", font=F["body"], bg=C["white"],
                 fg=C["text"], anchor="e", wraplength=180, justify="right"
                 ).grid(row=row+1, column=col, sticky="e", padx=(4, 8), pady=(0, 4))

    def _build_info_display(self, emp):
        f = self.info_frame
        for w in f.winfo_children():
            if w != self.photo_canvas:
                w.destroy()

        def v(k): return emp.get(k, "") or ""

        self._sec(f, T["sec_basic"], 0)
        self._row(f, T["f_emp_id"],      v("employee_id"),      2, 3)
        self._row(f, T["f_first_name"],  v("first_name"),       2, 2)
        self._row(f, T["f_last_name"],   v("last_name"),        2, 1)
        self._row(f, T["f_dob"],         v("date_of_birth"),    4, 3)
        self._row(f, T["f_gender"],      v("gender"),           4, 2)
        self._row(f, T["f_nationality"], v("nationality"),      4, 1)
        self._row(f, T["f_national_id"], v("national_id"),      6, 3)
        self._row(f, T["f_passport"],    v("passport_number"),  6, 2)
        self._row(f, T["f_marital"],     v("marital_status"),   6, 1)

        self._sec(f, T["sec_contact"], 8)
        self._row(f, T["f_phone"],    v("phone"),                    10, 3)
        self._row(f, T["f_email"],    v("email"),                    10, 2)
        self._row(f, T["f_address"],  v("address"),                  10, 1)
        self._row(f, T["f_ec_name"],  v("emergency_contact_name"),   12, 3)
        self._row(f, T["f_ec_phone"], v("emergency_contact_phone"),  12, 2)

        self._sec(f, T["sec_job"], 14)
        self._row(f, T["f_department"], v("department"),      16, 3)
        self._row(f, T["f_job_title"],  v("job_title"),       16, 2)
        self._row(f, T["f_emp_type"],   v("employment_type"), 16, 1)
        self._row(f, T["f_hire_date"],  v("hire_date"),       18, 3)
        self._row(f, T["f_salary"],     v("salary"),          18, 2)
        self._row(f, T["f_manager"],    v("manager"),         18, 1)
        self._row(f, T["f_location"],   v("work_location"),   20, 3)

        self._sec(f, T["sec_family"], 22)
        self._row(f, T["f_spouse"],       v("spouse_name"),   24, 3)
        self._row(f, T["f_children"],     v("children_count"),24, 2)
        self._row(f, T["f_family_notes"], v("family_notes"),  24, 1)

        self._sec(f, T["sec_notes"], 26)
        tk.Label(f, text=v("notes") or "—", font=F["body"],
                 bg=C["white"], fg=C["text"], wraplength=520,
                 justify="right", anchor="e"
                 ).grid(row=28, column=0, columnspan=4, sticky="e",
                         padx=(4, 8), pady=4)

        meta = f"  تاريخ الإضافة: {v('created_at')[:10]}   |   آخر تحديث: {v('updated_at')[:10]}"
        tk.Label(f, text=meta, font=F["tiny"], bg=C["white"],
                 fg=C["subtext"], anchor="e"
                 ).grid(row=30, column=0, columnspan=4, sticky="e",
                         padx=(4, 8), pady=(10, 6))

        # Re-position photo
        self.photo_canvas.grid(row=2, column=0, rowspan=10,
                                sticky="n", padx=16, pady=16)

    # ── Docs tab ──────────────────────────────────────────────────────────────

    def _build_docs_tab(self):
        # Toolbar
        tb = tk.Frame(self.docs_tab, bg=C["section_bg"],
                      highlightthickness=1, highlightbackground=C["border"])
        tb.pack(fill="x", padx=12, pady=(12, 0))

        inner_tb = tk.Frame(tb, bg=C["section_bg"])
        inner_tb.pack(fill="x", padx=10, pady=8)

        tk.Button(inner_tb, text=T["btn_upload_doc"], command=self._upload_doc,
                  bg=C["accent"], fg="white", font=F["small"],
                  relief="flat", padx=12, pady=6, cursor="hand2",
                  activebackground=C["accent_hover"],
                  activeforeground="white").pack(side="left", padx=(0, 10))

        self.doc_name_var = tk.StringVar()
        nf = tk.Frame(inner_tb, bg=C["input_border"], padx=1, pady=1)
        nf.pack(side="left", padx=(0, 6))
        tk.Entry(nf, textvariable=self.doc_name_var, width=20,
                 font=F["body"], bd=0, bg=C["input_bg"],
                 fg=C["text"], justify="right").pack(padx=4, pady=3)

        tk.Label(inner_tb, text=f"{T['doc_name_label']}",
                 font=F["small"], bg=C["section_bg"],
                 fg=C["subtext"]).pack(side="left", padx=4)

        self.doc_type_var = tk.StringVar(value=T["doc_types"][0])
        ttk.Combobox(inner_tb, textvariable=self.doc_type_var,
                     values=T["doc_types"], width=14,
                     font=F["body"], state="readonly",
                     justify="right").pack(side="right", padx=4)
        tk.Label(inner_tb, text=f"{T['doc_type_label']}",
                 font=F["small"], bg=C["section_bg"],
                 fg=C["subtext"]).pack(side="right", padx=4)

        # Table
        style = ttk.Style()
        style.configure("Docs.Treeview", rowheight=36, font=F["body"])
        style.configure("Docs.Treeview.Heading", font=F["small"])

        cols = ("doc_type", "doc_name", "uploaded_at", "file")
        self.doc_tree = ttk.Treeview(self.docs_tab, columns=cols,
                                      show="headings", style="Docs.Treeview")
        for col, text, w, anc in [
            ("doc_type",    T["doc_type"], 130, "e"),
            ("doc_name",    T["doc_name"], 230, "e"),
            ("uploaded_at", T["doc_date"], 120, "center"),
            ("file",        T["doc_file"], 200, "w"),
        ]:
            self.doc_tree.heading(col, text=text, anchor=anc)
            self.doc_tree.column(col, width=w, anchor=anc)

        dsb = ttk.Scrollbar(self.docs_tab, orient="vertical",
                             command=self.doc_tree.yview)
        self.doc_tree.configure(yscrollcommand=dsb.set)
        self.doc_tree.pack(side="left", fill="both", expand=True,
                            padx=(12, 0), pady=10)
        dsb.pack(side="right", fill="y", pady=10, padx=(0, 12))

        self.doc_tree.bind("<Double-1>", self._open_doc)

        dm = tk.Menu(self.window, tearoff=0, font=F["body"])
        dm.add_command(label=T["btn_open_folder"], command=self._open_doc)
        dm.add_command(label=T["btn_delete_doc"],  command=self._delete_doc)
        self.doc_tree.bind("<Button-3>", lambda e: (
            self.doc_tree.selection_set(self.doc_tree.identify_row(e.y)),
            dm.post(e.x_root, e.y_root)
        ))

    # ── Data loading ──────────────────────────────────────────────────────────

    def _load(self):
        emp = self.db.get_employee(self.employee_id)
        if not emp:
            return
        name = f"{emp.get('first_name','') or ''} {emp.get('last_name','') or ''}".strip()
        self.name_lbl.configure(text=f"👤  {name}  ")
        self.window.title(name)
        self._build_info_display(emp)
        self._load_photo(emp.get("photo_path"))
        self._load_docs()

    def _load_photo(self, path):
        self.photo_canvas.delete("all")
        if not path or not os.path.exists(path):
            self.photo_canvas.create_text(65, 65, text=T["no_photo"],
                                          fill=C["subtext"], font=F["small"])
            return
        if not PIL_AVAILABLE:
            self.photo_canvas.create_text(65, 65, text="📷",
                                          fill=C["accent"], font=("Segoe UI", 30))
            return
        try:
            img = Image.open(path)
            img = img.convert("RGB") if img.mode not in ("RGB","RGBA") else img
            img.thumbnail((130, 130), Image.LANCZOS)
            self._photo_image = ImageTk.PhotoImage(img)
            self.photo_canvas.create_image(65, 65, anchor="center",
                                           image=self._photo_image)
        except Exception:
            self.photo_canvas.create_text(65, 65, text=T["photo_error"],
                                          fill=C["danger"], font=F["small"])

    def _load_docs(self):
        self.doc_tree.delete(*self.doc_tree.get_children())
        self._docs_map = {}
        for doc in self.db.get_documents(self.employee_id):
            fname = os.path.basename(doc["file_path"])
            date  = (doc["uploaded_at"] or "")[:10]
            iid   = str(doc["id"])
            self.doc_tree.insert("", "end", iid=iid, values=(
                doc.get("doc_type",""),
                doc.get("doc_name",""),
                date, fname
            ))
            self._docs_map[iid] = doc

    # ── Actions ───────────────────────────────────────────────────────────────

    def _upload_doc(self):
        path = filedialog.askopenfilename(
            filetypes=[("Documents & Images",
                        "*.pdf *.jpg *.jpeg *.png *.docx *.doc *.xlsx *.txt *.bmp"),
                       ("All files", "*.*")]
        )
        if not path:
            return
        doc_type = self.doc_type_var.get()
        doc_name = self.doc_name_var.get().strip() or \
                   os.path.splitext(os.path.basename(path))[0]
        try:
            self.db.add_document(self.employee_id, path, doc_name, doc_type)
            self._load_docs()
            self.doc_name_var.set("")
        except Exception as e:
            messagebox.showerror("", str(e), parent=self.window)

    def _open_doc(self, event=None):
        sel = self.doc_tree.focus()
        if not sel or sel not in self._docs_map:
            return
        fp = self._docs_map[sel]["file_path"]
        if not os.path.exists(fp):
            messagebox.showerror("", "الملف غير موجود.", parent=self.window)
            return
        try:
            if platform.system() == "Windows":
                os.startfile(fp)
            elif platform.system() == "Darwin":
                subprocess.call(["open", fp])
            else:
                subprocess.call(["xdg-open", fp])
        except Exception as e:
            messagebox.showerror("", str(e), parent=self.window)

    def _delete_doc(self):
        sel = self.doc_tree.focus()
        if not sel or sel not in self._docs_map:
            return
        doc = self._docs_map[sel]
        msg = T["del_doc_confirm"].format(name=doc["doc_name"])
        if messagebox.askyesno("", msg, parent=self.window):
            self.db.delete_document(doc["id"])
            self._load_docs()

    def _edit(self):
        def after():
            self._load()
            if self.on_update:
                self.on_update()
        EmployeeForm(self.window, self.db,
                     employee_id=self.employee_id, on_save=after)
