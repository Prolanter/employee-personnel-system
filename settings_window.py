"""Settings window — Arabic RTL, modern UI."""

import tkinter as tk
from tkinter import ttk, messagebox
from lang import C, F, T


class SettingsWindow:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db

        self.window = tk.Toplevel(parent)
        self.window.title(T["settings_title"])
        self.window.geometry("580x500")
        self.window.resizable(False, False)
        self.window.configure(bg=C["bg"])
        self._center()
        self._build_ui()
        self.window.grab_set()

    def _center(self):
        self.window.update_idletasks()
        w, h = 580, 500
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _build_ui(self):
        hdr = tk.Frame(self.window, bg=C["topbar"], height=52)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text=f"  {T['settings_title']}  ⚙",
                 font=F["h2"], bg=C["topbar"], fg="white").pack(side="right", padx=16)

        nb = ttk.Notebook(self.window)
        nb.pack(fill="both", expand=True, padx=12, pady=12)

        ut = tk.Frame(nb, bg=C["white"]); nb.add(ut, text=T["tab_users"])
        pt = tk.Frame(nb, bg=C["white"]); nb.add(pt, text=T["tab_password"])
        at = tk.Frame(nb, bg=C["white"]); nb.add(at, text=T["tab_about"])

        self._users_tab(ut)
        self._pw_tab(pt)
        self._about_tab(at)

    # ── Users ─────────────────────────────────────────────────────────────────

    def _users_tab(self, parent):
        f = tk.Frame(parent, bg=C["white"], padx=18, pady=14)
        f.pack(fill="both", expand=True)

        tk.Label(f, text=T["system_users"], font=F["h3"],
                 bg=C["white"], fg=C["text"], anchor="e").pack(fill="x")

        self.user_tree = ttk.Treeview(f, columns=("u", "d"), show="headings", height=7)
        self.user_tree.heading("u", text=T["user_col"],    anchor="e")
        self.user_tree.heading("d", text=T["created_col"], anchor="center")
        self.user_tree.column("u", width=220, anchor="e")
        self.user_tree.column("d", width=160, anchor="center")
        self.user_tree.pack(fill="x", pady=8)
        self._load_users()

        # Add user
        add_box = tk.LabelFrame(f, text=T["add_user_lbl"],
                                 bg=C["white"], font=F["small"],
                                 fg=C["subtext"], labelanchor="e")
        add_box.pack(fill="x", pady=8)
        row = tk.Frame(add_box, bg=C["white"])
        row.pack(padx=10, pady=8, fill="x")

        tk.Button(row, text=T["btn_add_user"], command=self._add_user,
                  bg=C["accent"], fg="white", font=F["small"],
                  relief="flat", padx=12, pady=5, cursor="hand2").pack(side="left")

        self.new_pw_var = tk.StringVar()
        pf = tk.Frame(row, bg=C["input_border"], padx=1, pady=1)
        pf.pack(side="right", padx=4)
        tk.Entry(pf, textvariable=self.new_pw_var, show="●", width=16,
                 font=F["body"], bd=0, bg=C["input_bg"],
                 fg=C["text"], justify="right").pack(padx=3, pady=3)
        tk.Label(row, text=T["password_lbl"], font=F["small"],
                 bg=C["white"], fg=C["subtext"]).pack(side="right", padx=4)

        self.new_user_var = tk.StringVar()
        uf = tk.Frame(row, bg=C["input_border"], padx=1, pady=1)
        uf.pack(side="right", padx=4)
        tk.Entry(uf, textvariable=self.new_user_var, width=16,
                 font=F["body"], bd=0, bg=C["input_bg"],
                 fg=C["text"], justify="right").pack(padx=3, pady=3)
        tk.Label(row, text=T["username_lbl"], font=F["small"],
                 bg=C["white"], fg=C["subtext"]).pack(side="right", padx=4)

        tk.Button(f, text=T["btn_del_user"], command=self._del_user,
                  bg=C["danger"], fg="white", font=F["small"],
                  relief="flat", padx=12, pady=6, cursor="hand2").pack(anchor="e", pady=4)

    def _load_users(self):
        self.user_tree.delete(*self.user_tree.get_children())
        for u in self.db.get_users():
            self.user_tree.insert("", "end", iid=str(u["id"]),
                                  values=(u["username"],
                                          (u["created_at"] or "")[:10]))

    def _add_user(self):
        uname = self.new_user_var.get().strip()
        pw    = self.new_pw_var.get().strip()
        if not uname or not pw:
            messagebox.showwarning("", "اسم المستخدم وكلمة المرور مطلوبان.", parent=self.window)
            return
        if len(pw) < 6:
            messagebox.showwarning("", "كلمة المرور يجب أن تكون 6 أحرف على الأقل.", parent=self.window)
            return
        if self.db.add_user(uname, pw):
            self._load_users()
            self.new_user_var.set("")
            self.new_pw_var.set("")
            messagebox.showinfo("", f"تم إضافة المستخدم '{uname}'.", parent=self.window)
        else:
            messagebox.showerror("", "اسم المستخدم موجود مسبقاً.", parent=self.window)

    def _del_user(self):
        sel = self.user_tree.focus()
        if not sel:
            messagebox.showwarning("", "الرجاء تحديد مستخدم.", parent=self.window)
            return
        uname = self.user_tree.item(sel, "values")[0]
        if uname == "admin":
            messagebox.showwarning("", "لا يمكن حذف المستخدم admin.", parent=self.window)
            return
        if messagebox.askyesno("", f"حذف المستخدم '{uname}'؟", parent=self.window):
            self.db.delete_user(int(sel))
            self._load_users()

    # ── Password ──────────────────────────────────────────────────────────────

    def _pw_tab(self, parent):
        f = tk.Frame(parent, bg=C["white"], padx=30, pady=20)
        f.pack(fill="both", expand=True)

        tk.Label(f, text=T["change_pw_title"], font=F["h3"],
                 bg=C["white"], fg=C["text"], anchor="e").pack(fill="x", pady=(0, 16))

        for label, attr, show in [
            (T["username_lbl"], "cp_user", ""),
            (T["new_pw"],       "cp_pw",   "●"),
            (T["confirm_pw"],   "cp_pw2",  "●"),
        ]:
            tk.Label(f, text=label, font=F["small"],
                     bg=C["white"], fg=C["subtext"], anchor="e").pack(fill="x")
            var = tk.StringVar()
            setattr(self, attr, var)
            fr = tk.Frame(f, bg=C["input_border"], padx=1, pady=1)
            fr.pack(fill="x", pady=(2, 10))
            tk.Entry(fr, textvariable=var, show=show, font=F["body"],
                     bd=0, bg=C["input_bg"], fg=C["text"],
                     justify="right").pack(fill="x", padx=4, pady=4)

        tk.Button(f, text=T["btn_change_pw"], command=self._change_pw,
                  bg=C["accent"], fg="white", font=F["h3"],
                  relief="flat", padx=18, pady=8, cursor="hand2",
                  activebackground=C["accent_hover"],
                  activeforeground="white").pack(anchor="e")

    def _change_pw(self):
        uname = self.cp_user.get().strip()
        pw    = self.cp_pw.get().strip()
        pw2   = self.cp_pw2.get().strip()
        if not uname or not pw:
            messagebox.showwarning("", "جميع الحقول مطلوبة.", parent=self.window)
            return
        if pw != pw2:
            messagebox.showerror("", "كلمتا المرور غير متطابقتين.", parent=self.window)
            return
        if len(pw) < 6:
            messagebox.showwarning("", "كلمة المرور يجب أن تكون 6 أحرف على الأقل.", parent=self.window)
            return
        self.db.change_password(uname, pw)
        messagebox.showinfo("", f"تم تغيير كلمة المرور للمستخدم '{uname}'.", parent=self.window)
        for a in ("cp_user", "cp_pw", "cp_pw2"):
            getattr(self, a).set("")

    # ── About ─────────────────────────────────────────────────────────────────

    def _about_tab(self, parent):
        f = tk.Frame(parent, bg=C["white"])
        f.pack(fill="both", expand=True)
        tk.Label(f, text="🏢", font=("Segoe UI", 44),
                 bg=C["white"]).pack(pady=(28, 6))
        tk.Label(f, text=T["app_title"], font=F["h1"],
                 bg=C["white"], fg=C["topbar"]).pack()
        tk.Label(f, text=T["about_version"], font=F["body"],
                 bg=C["white"], fg=C["subtext"]).pack(pady=4)
        tk.Label(f, text=T["about_text"], font=F["small"],
                 bg=C["white"], fg=C["text"], justify="right").pack(padx=30, pady=10)
