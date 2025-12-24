import tkinter as tk
from tkinter import messagebox
import mysql.connector


def open_register_window():
    def register_user():
        username = entry_username.get()
        password = entry_password.get()
        confirm_password = entry_confirm.get()
        
        if username == "" or password == "" or confirm_password == "":
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
            
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="diabetes_app"
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Account created successfully!\nYou can now login.")
            register_win.destroy()
            # إعادة فتح Login
            from login import open_login_window
            open_login_window()
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_enter(e):
        e.widget['background'] = '#6B6BFF'

    def on_leave(e):
        e.widget['background'] = '#5A5AFF'

    def back_to_login():
        register_win.destroy()
        from login import open_login_window
        open_login_window()

    register_win = tk.Tk()
    register_win.title("Register - Diabetes AI")
    register_win.geometry("500x650")
    register_win.configure(bg="#1E1E2F")
    register_win.resizable(False, False)

    # Header Frame
    header_frame = tk.Frame(register_win, bg="#2A2A3F", height=120)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)

    tk.Label(
        header_frame, 
        text="📝",
        font=("Segoe UI", 50),
        bg="#2A2A3F",
        fg="#FFFFFF"
    ).pack(pady=(20, 5))

    tk.Label(
        header_frame, 
        text="Create Your Account",
        font=("Segoe UI", 16, "bold"),
        bg="#2A2A3F",
        fg="#AAAAAA"
    ).pack()

    # Main Content Frame
    content_frame = tk.Frame(register_win, bg="#1E1E2F")
    content_frame.pack(fill="both", expand=True, padx=50, pady=30)

    tk.Label(
        content_frame, 
        text="Join Us Today!",
        font=("Segoe UI", 28, "bold"),
        fg="#FFFFFF",
        bg="#1E1E2F"
    ).pack(pady=(0, 10))

    tk.Label(
        content_frame, 
        text="Start monitoring your health with AI",
        font=("Segoe UI", 12),
        fg="#AAAAAA",
        bg="#1E1E2F"
    ).pack(pady=(0, 30))

    # Username Field
    tk.Label(
        content_frame, 
        text="Username",
        font=("Segoe UI", 12, "bold"),
        fg="#FFFFFF",
        bg="#1E1E2F"
    ).pack(anchor="w", pady=(0, 5))

    username_frame = tk.Frame(content_frame, bg="#2E2E3F", highlightbackground="#3A3A4F", highlightthickness=2)
    username_frame.pack(fill="x", pady=(0, 15))

    entry_username = tk.Entry(
        username_frame,
        font=("Segoe UI", 14),
        bg="#2E2E3F",
        fg="#FFFFFF",
        insertbackground="#FFFFFF",
        relief="flat",
        bd=10
    )
    entry_username.pack(fill="both", expand=True)

    # Password Field
    tk.Label(
        content_frame, 
        text="Password",
        font=("Segoe UI", 12, "bold"),
        fg="#FFFFFF",
        bg="#1E1E2F"
    ).pack(anchor="w", pady=(0, 5))

    password_frame = tk.Frame(content_frame, bg="#2E2E3F", highlightbackground="#3A3A4F", highlightthickness=2)
    password_frame.pack(fill="x", pady=(0, 15))

    entry_password = tk.Entry(
        password_frame,
        show="●",
        font=("Segoe UI", 14),
        bg="#2E2E3F",
        fg="#FFFFFF",
        insertbackground="#FFFFFF",
        relief="flat",
        bd=10
    )
    entry_password.pack(fill="both", expand=True)

    # Confirm Password Field
    tk.Label(
        content_frame, 
        text="Confirm Password",
        font=("Segoe UI", 12, "bold"),
        fg="#FFFFFF",
        bg="#1E1E2F"
    ).pack(anchor="w", pady=(0, 5))

    confirm_frame = tk.Frame(content_frame, bg="#2E2E3F", highlightbackground="#3A3A4F", highlightthickness=2)
    confirm_frame.pack(fill="x", pady=(0, 25))

    entry_confirm = tk.Entry(
        confirm_frame,
        show="●",
        font=("Segoe UI", 14),
        bg="#2E2E3F",
        fg="#FFFFFF",
        insertbackground="#FFFFFF",
        relief="flat",
        bd=10
    )
    entry_confirm.pack(fill="both", expand=True)
    entry_confirm.bind('<Return>', lambda e: register_user())

    # Register Button
    register_button = tk.Button(
        content_frame,
        text="Create Account",
        font=("Segoe UI", 16, "bold"),
        bg="#5A5AFF",
        fg="#FFFFFF",
        command=register_user,
        relief="flat",
        cursor="hand2",
        activebackground="#6B6BFF",
        activeforeground="#FFFFFF",
        bd=0,
        padx=20,
        pady=15
    )
    register_button.pack(fill="x", pady=(0, 15))
    register_button.bind("<Enter>", on_enter)
    register_button.bind("<Leave>", on_leave)

    # Back to Login
    back_frame = tk.Frame(content_frame, bg="#1E1E2F")
    back_frame.pack(pady=10)

    tk.Label(
        back_frame,
        text="Already have an account?",
        font=("Segoe UI", 11),
        bg="#1E1E2F",
        fg="#AAAAAA"
    ).pack(side="left", padx=(0, 5))

    back_label = tk.Label(
        back_frame,
        text="Login here",
        font=("Segoe UI", 11, "bold", "underline"),
        bg="#1E1E2F",
        fg="#5A5AFF",
        cursor="hand2"
    )
    back_label.pack(side="left")
    back_label.bind("<Button-1>", lambda e: back_to_login())

    # Footer
    footer = tk.Frame(register_win, bg="#2A2A3F", height=50)
    footer.pack(fill="x", side="bottom")
    footer.pack_propagate(False)

    tk.Label(
        footer,
        text="© 2024 Diabetes AI - Your Health, Our Priority",
        font=("Segoe UI", 9),
        bg="#2A2A3F",
        fg="#666666"
    ).pack(pady=15)

    register_win.mainloop()