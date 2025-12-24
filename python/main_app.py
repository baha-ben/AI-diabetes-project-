import tkinter as tk
from tkinter import messagebox
import joblib
import mysql.connector
from history import open_history_page

model = joblib.load("python/diabetes_model.pkl")


def open_main_app(user_id):
    # Get username from database
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="diabetes_app"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE id=%s", (user_id,))
        result = cursor.fetchone()
        username = result[0] if result else "User"
        conn.close()
    except:
        username = "User"

    window = tk.Tk()
    window.title("Diabetes AI Predictor")
    window.geometry("800x950")
    window.configure(bg="#1E1E2F")
    window.resizable(True, True)

    # Main Container with Scrollbar
    main_canvas = tk.Canvas(window, bg="#1E1E2F", highlightthickness=0)
    scrollbar = tk.Scrollbar(window, orient="vertical", command=main_canvas.yview)
    scrollable_frame = tk.Frame(main_canvas, bg="#1E1E2F")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
    )

    main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=800)
    main_canvas.configure(yscrollcommand=scrollbar.set)

    # Mouse wheel scrolling
    def _on_mousewheel(event):
        main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    window.bind_all("<MouseWheel>", _on_mousewheel)

    # Pack canvas and scrollbar
    main_canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # === HEADER ===
    header_frame = tk.Frame(scrollable_frame, bg="#2A2A3F")
    header_frame.pack(fill="x")

    # Top Bar with User Info
    top_bar = tk.Frame(header_frame, bg="#2A2A3F")
    top_bar.pack(fill="x", padx=40, pady=20)

    # Left: User Profile
    left_section = tk.Frame(top_bar, bg="#2A2A3F")
    left_section.pack(side="left", fill="x", expand=True)

    # Avatar
    avatar_canvas = tk.Canvas(left_section, width=55, height=55, bg="#2A2A3F", highlightthickness=0)
    avatar_canvas.pack(side="left", padx=(0, 15))
    avatar_canvas.create_oval(5, 5, 50, 50, fill="#5A5AFF", outline="#7B7BFF", width=3)
    avatar_canvas.create_text(27, 27, text="👤", font=("Segoe UI", 22))

    # User Text Info
    user_text_frame = tk.Frame(left_section, bg="#2A2A3F")
    user_text_frame.pack(side="left", fill="y")

    tk.Label(
        user_text_frame,
        text=f"Welcome back, {username}! 👋",
        font=("Segoe UI", 15, "bold"),
        bg="#2A2A3F",
        fg="#FFFFFF",
        anchor="w"
    ).pack(anchor="w", pady=(5, 2))

    tk.Label(
        user_text_frame,
        text="Let's check your health status today",
        font=("Segoe UI", 10),
        bg="#2A2A3F",
        fg="#AAAAAA",
        anchor="w"
    ).pack(anchor="w")

    # Right: Logout Button
    def logout():
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            window.destroy()
            from login import open_login_window
            open_login_window()

    logout_btn = tk.Button(
        top_bar,
        text="🚪 Logout",
        font=("Segoe UI", 11, "bold"),
        bg="#FF6B6B",
        fg="#FFFFFF",
        relief="flat",
        cursor="hand2",
        command=logout,
        activebackground="#FF7B7B",
        padx=20,
        pady=10
    )
    logout_btn.pack(side="right", padx=10)

    # Title
    tk.Label(
        header_frame,
        text="🏥 Diabetes AI Predictor",
        font=("Segoe UI", 24, "bold"),
        bg="#2A2A3F",
        fg="#FFFFFF",
        pady=20
    ).pack()

    # ==================== MAIN CONTENT ====================
    main_frame = tk.Frame(scrollable_frame, bg="#1E1E2F")
    main_frame.pack(fill="both", expand=True, padx=40, pady=20)

    # Info Card
    info_frame = tk.Frame(main_frame, bg="#2A2A3F", highlightbackground="#3A3A4F", highlightthickness=2)
    info_frame.pack(fill="x", pady=(0, 20))

    tk.Label(
        info_frame,
        text="ℹ️ Enter your health information below for AI analysis",
        font=("Segoe UI", 12),
        bg="#2A2A3F",
        fg="#AAAAAA",
        pady=15
    ).pack()

    # Form Container
    form_container = tk.Frame(main_frame, bg="#1E1E2F")
    form_container.pack(fill="both", expand=True)

    labels_info = [
        ("👶 Pregnancies", "Number of pregnancies"),
        ("🩸 Glucose Level", "Blood glucose concentration"),
        ("💓 Blood Pressure", "Diastolic blood pressure (mm Hg)"),
        ("📏 Skin Thickness", "Triceps skin fold thickness (mm)"),
        ("💉 Insulin", "2-Hour serum insulin (mu U/ml)"),
        ("⚖️ BMI", "Body Mass Index (weight/height²)"),
        ("🧬 Pedigree Function", "Diabetes pedigree function"),
        ("👤 Age", "Age in years")
    ]
    
    entries = []

    def validate_number(value):
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    vcmd = (window.register(validate_number), "%P")

    # Create form fields
    for label_text, tooltip in labels_info:
        field_frame = tk.Frame(form_container, bg="#1E1E2F")
        field_frame.pack(fill="x", pady=6)

        # Label with tooltip
        label_container = tk.Frame(field_frame, bg="#1E1E2F")
        label_container.pack(fill="x", pady=(0, 5))

        tk.Label(
            label_container,
            text=label_text,
            font=("Segoe UI", 11, "bold"),
            anchor="w",
            bg="#1E1E2F",
            fg="#FFFFFF"
        ).pack(side="left")

        tk.Label(
            label_container,
            text=f"  ({tooltip})",
            font=("Segoe UI", 9, "italic"),
            anchor="w",
            bg="#1E1E2F",
            fg="#888888"
        ).pack(side="left")

        # Entry field
        entry_frame = tk.Frame(field_frame, bg="#2E2E3F", highlightbackground="#3A3A4F", highlightthickness=2)
        entry_frame.pack(fill="x")

        entry = tk.Entry(
            entry_frame,
            font=("Segoe UI", 12),
            validate="key",
            validatecommand=vcmd,
            bg="#2E2E3F",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            relief="flat",
            bd=7
        )
        entry.pack(fill="both", expand=True)
        entries.append(entry)

    def predict():
        values = []
        for entry in entries:
            if entry.get() == "":
                messagebox.showerror("Input Error", "⚠️ Please fill all fields with numeric values.")
                return
            values.append(float(entry.get()))
        
        result = model.predict([values])[0]
        result_text = "Diabetic" if result == 1 else "Not Diabetic"
        
        # Update result display
        if result == 1:
            result_label.config(
                text=f"⚠️ Result: {result_text}",
                fg="#FFFFFF",
                bg="#FF4C4C"
            )
            advice_label.config(
                text="Please consult with a healthcare professional for proper diagnosis and treatment.",
                fg="#FFAAAA"
            )
        else:
            result_label.config(
                text=f"✅ Result: {result_text}",
                fg="#FFFFFF",
                bg="#4CFF88"
            )
            advice_label.config(
                text="Keep maintaining a healthy lifestyle and regular checkups!",
                fg="#AAFFAA"
            )

        # Save to database
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="diabetes_app"
            )
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO diabetes_data
                (user_id, pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, pedigree, age, result)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (user_id, *values, result_text))
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_fields():
        for entry in entries:
            entry.delete(0, tk.END)
        result_label.config(text="", bg="#1E1E2F")
        advice_label.config(text="")

    # Buttons Frame
    buttons_frame = tk.Frame(main_frame, bg="#1E1E2F")
    buttons_frame.pack(fill="x", pady=20)

    # Predict Button
    predict_btn = tk.Button(
        buttons_frame,
        text="🔍 Predict Now",
        font=("Segoe UI", 15, "bold"),
        bg="#5A5AFF",
        fg="#FFFFFF",
        command=predict,
        relief="flat",
        cursor="hand2",
        activebackground="#6B6BFF",
        bd=0,
        padx=20,
        pady=14
    )
    predict_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

    # Clear Button
    clear_btn = tk.Button(
        buttons_frame,
        text="🔄 Clear",
        font=("Segoe UI", 13, "bold"),
        bg="#FF6B6B",
        fg="#FFFFFF",
        command=clear_fields,
        relief="flat",
        cursor="hand2",
        activebackground="#FF7B7B",
        bd=0,
        padx=20,
        pady=14
    )
    clear_btn.pack(side="left", fill="x", expand=True, padx=(5, 0))

    # Result Display
    result_frame = tk.Frame(main_frame, bg="#1E1E2F")
    result_frame.pack(fill="x", pady=15)

    result_label = tk.Label(
        result_frame,
        text="",
        font=("Segoe UI", 19, "bold"),
        bg="#1E1E2F",
        pady=18
    )
    result_label.pack(fill="x")

    advice_label = tk.Label(
        result_frame,
        text="",
        font=("Segoe UI", 11, "italic"),
        bg="#1E1E2F",
        wraplength=650
    )
    advice_label.pack(fill="x", pady=(0, 10))

    # History Button
    history_btn = tk.Button(
        main_frame,
        text="📊 View Health History",
        font=("Segoe UI", 14, "bold"),
        bg="#3FA9F5",
        fg="#FFFFFF",
        relief="flat",
        cursor="hand2",
        command=lambda: open_history_page(user_id),
        activebackground="#4FB9FF",
        bd=0,
        padx=20,
        pady=13
    )
    history_btn.pack(fill="x", pady=(10, 20))

    # Footer
    footer = tk.Frame(scrollable_frame, bg="#2A2A3F")
    footer.pack(fill="x", side="bottom")

    tk.Label(
        footer,
        text="🤖 Powered by Machine Learning & Artificial Intelligence",
        font=("Segoe UI", 10, "italic"),
        bg="#2A2A3F",
        fg="#888888",
        pady=20
    ).pack()

    window.mainloop()