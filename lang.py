"""
Arabic language strings and shared UI constants.
All text is in Arabic. Layout is RTL.
"""

# ── Colours ───────────────────────────────────────────────────────────────────
C = {
    "bg":           "#F0F4F8",   # soft blue-grey background
    "white":        "#FFFFFF",
    "card":         "#FFFFFF",
    "topbar":       "#1B2A4A",   # deep navy
    "topbar2":      "#243656",
    "accent":       "#2563EB",   # vivid blue
    "accent_hover": "#1D4ED8",
    "accent_light": "#EFF6FF",
    "success":      "#16A34A",
    "danger":       "#DC2626",
    "warning":      "#D97706",
    "text":         "#1E293B",
    "subtext":      "#64748B",
    "border":       "#CBD5E1",
    "section_bg":   "#F1F5F9",
    "section_fg":   "#1B2A4A",
    "row_alt":      "#F8FAFC",
    "input_bg":     "#F8FAFC",
    "input_border": "#94A3B8",
    "selected":     "#2563EB",
}

# ── Fonts ─────────────────────────────────────────────────────────────────────
# "Segoe UI" renders Arabic well on Windows
F = {
    "h1":    ("Segoe UI", 15, "bold"),
    "h2":    ("Segoe UI", 12, "bold"),
    "h3":    ("Segoe UI", 11, "bold"),
    "body":  ("Segoe UI", 10),
    "small": ("Segoe UI", 9),
    "tiny":  ("Segoe UI", 8),
}

# ── Arabic Text Strings ───────────────────────────────────────────────────────
T = {
    # App
    "app_title":        "نظام ملفات الموظفين",
    "app_subtitle":     "سجلات الموظفين الإلكترونية",

    # Top bar
    "add_employee":     "+ إضافة موظف",
    "backup":           "💾 نسخ احتياطي",
    "settings":         "⚙ الإعدادات",

    # Search
    "search_hint":      "البحث بالاسم أو رقم الهوية...",
    "clear":            "✕",

    # Table headers
    "emp_id":           "رقم الموظف",
    "full_name":        "الاسم الكامل",
    "department":       "القسم",
    "job_title":        "المسمى الوظيفي",
    "phone":            "الهاتف",
    "status":           "الحالة",

    # Status bar
    "employees_found":  "موظف",
    "ready":            "جاهز",

    # Context menu
    "view_edit":        "👁 عرض / تعديل",
    "delete_emp":       "🗑 حذف الموظف",

    # Form titles
    "add_emp_title":    "إضافة موظف جديد",
    "edit_emp_title":   "تعديل بيانات الموظف",

    # Sections
    "sec_basic":        "📋  المعلومات الأساسية",
    "sec_contact":      "📞  معلومات الاتصال",
    "sec_job":          "💼  المعلومات الوظيفية",
    "sec_family":       "👨‍👩‍👧  معلومات الأسرة",
    "sec_notes":        "📝  ملاحظات",

    # Fields
    "f_emp_id":         "رقم الموظف *",
    "f_first_name":     "الاسم الأول *",
    "f_last_name":      "اسم العائلة *",
    "f_dob":            "تاريخ الميلاد (YYYY-MM-DD)",
    "f_gender":         "الجنس",
    "f_nationality":    "الجنسية",
    "f_national_id":    "رقم الهوية الوطنية",
    "f_passport":       "رقم جواز السفر",
    "f_marital":        "الحالة الاجتماعية",
    "f_phone":          "رقم الهاتف",
    "f_email":          "البريد الإلكتروني",
    "f_address":        "العنوان",
    "f_ec_name":        "اسم جهة الاتصال في الطوارئ",
    "f_ec_phone":       "هاتف جهة الاتصال في الطوارئ",
    "f_department":     "القسم",
    "f_job_title":      "المسمى الوظيفي",
    "f_emp_type":       "نوع التوظيف",
    "f_hire_date":      "تاريخ التعيين (YYYY-MM-DD)",
    "f_salary":         "الراتب",
    "f_manager":        "المدير المباشر",
    "f_location":       "موقع العمل",
    "f_spouse":         "اسم الزوج/الزوجة",
    "f_children":       "عدد الأبناء",
    "f_family_notes":   "ملاحظات عائلية",
    "f_notes":          "ملاحظات عامة",

    # Buttons
    "btn_save":         "💾  حفظ",
    "btn_cancel":       "إلغاء",
    "btn_edit":         "✏  تعديل",
    "btn_close":        "✕  إغلاق",
    "btn_set_photo":    "📷 تعيين الصورة",
    "btn_upload_doc":   "+ رفع مستند",
    "btn_open_folder":  "📂 فتح الملف",
    "btn_delete_doc":   "🗑 حذف المستند",

    # Tabs
    "tab_info":         "👤  بيانات الموظف",
    "tab_docs":         "📁  المستندات",

    # Documents
    "doc_type":         "نوع المستند",
    "doc_name":         "اسم المستند",
    "doc_date":         "تاريخ الرفع",
    "doc_file":         "الملف",
    "doc_name_label":   "الاسم:",
    "doc_type_label":   "النوع:",

    # Photo
    "no_photo":         "لا توجد صورة",
    "photo_set":        "✓ تم تعيين الصورة",
    "photo_error":      "خطأ في الصورة",

    # Validation
    "val_name":         "الاسم الأول واسم العائلة مطلوبان.",
    "val_id":           "رقم الموظف مطلوب.",
    "saved_ok":         "تم حفظ بيانات الموظف بنجاح.",
    "save_err":         "تعذر الحفظ: ",

    # Delete
    "del_title":        "حذف الموظف",
    "del_confirm":      "هل تريد حذف الموظف '{name}' وجميع مستنداته؟\n\nلا يمكن التراجع عن هذا الإجراء.",
    "del_doc_confirm":  "هل تريد حذف '{name}'؟\nسيتم حذف الملف نهائياً.",
    "deleted":          "تم حذف الموظف '{name}'.",

    # Backup
    "backup_title":     "اختر مجلد النسخ الاحتياطي",
    "backup_ok":        "تم حفظ النسخ الاحتياطي في:\n{path}\n\nاحتفظ بملف personnel.key في مكان آمن.",
    "backup_fail":      "فشل النسخ الاحتياطي",
    "backup_done":      "اكتمل النسخ الاحتياطي",

    # Settings
    "settings_title":   "الإعدادات",
    "tab_users":        "👥  المستخدمون",
    "tab_password":     "🔑  تغيير كلمة المرور",
    "tab_about":        "ℹ  حول البرنامج",
    "system_users":     "مستخدمو النظام",
    "add_user_lbl":     "إضافة مستخدم جديد",
    "username_lbl":     "اسم المستخدم:",
    "password_lbl":     "كلمة المرور:",
    "btn_add_user":     "إضافة",
    "btn_del_user":     "🗑 حذف المستخدم المحدد",
    "change_pw_title":  "تغيير كلمة المرور",
    "new_pw":           "كلمة المرور الجديدة:",
    "confirm_pw":       "تأكيد كلمة المرور:",
    "btn_change_pw":    "تغيير كلمة المرور",
    "user_col":         "اسم المستخدم",
    "created_col":      "تاريخ الإنشاء",

    # Login
    "login_title":      "تسجيل الدخول — نظام ملفات الموظفين",
    "login_username":   "اسم المستخدم",
    "login_password":   "كلمة المرور",
    "login_btn":        "  دخول  ",
    "login_hint":       "الدخول الافتراضي: admin / admin123",
    "login_fail":       "اسم المستخدم أو كلمة المرور غير صحيحة.",
    "login_empty":      "الرجاء إدخال اسم المستخدم وكلمة المرور.",

    # About
    "about_version":    "الإصدار 1.0 — غير متصل بالإنترنت وآمن",
    "about_text": (
        "• جميع البيانات محفوظة محلياً — لا يتطلب اتصالاً بالإنترنت\n"
        "• قاعدة بيانات مشفرة باستخدام تشفير Fernet المتماثل\n"
        "• ملفات الموظفين منظمة في مجلدات منفصلة\n"
        "• نسخ احتياطي متاح في أي وقت\n\n"
        "بيانات الدخول الافتراضية: admin / admin123\n"
        "يرجى تغيير كلمة المرور بعد أول تسجيل دخول.\n\n"
        "Designed and Developed by Mustafa Kenji"

    ),

    # Dropdown values
    "departments": [
        "الموارد البشرية", "المالية", "تقنية المعلومات", "العمليات",
        "المبيعات", "التسويق", "الشؤون القانونية", "الإدارة",
        "الهندسة", "أخرى"
    ],
    "emp_types": ["دوام كامل", "دوام جزئي", "عقد", "مؤقت", "متدرب"],
    "genders":   ["ذكر", "أنثى"],
    "maritals":  ["أعزب/عزباء", "متزوج/متزوجة", "مطلق/مطلقة", "أرمل/أرملة"],
    "doc_types": [
        "جواز السفر", "الهوية الوطنية", "السيرة الذاتية", "العقد",
        "الشهادات", "صورة شخصية", "طبي", "أخرى"
    ],
}
