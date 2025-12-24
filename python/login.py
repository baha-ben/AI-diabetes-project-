import tkinter as tk
from tkinter import messagebox
from register import open_register_window
from main_app import open_main_app
import mysql.connector


def open_login_window():
    def login_user():
        username = entry_username.get()
        password = entry_password.get()
        
        if username == "" or password == "":
            messagebox.showerror("Error", "Please fill all fields")
            return
            
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="diabetes_app"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username=%s AND password=%s", (username, password))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                user_id = result[0]
                login_win.destroy()
                open_main_app(user_id)
            else:
                messagebox.showerror("Error", "Invalid username or password")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_enter(e):
        e.widget['background'] = '#6B6BFF'

    def on_leave(e):
        e.widget['background'] = '#5A5AFF'

    login_win = tk.Tk()
    login_win.title("Login - Diabetes AI")
    login_win.geometry("500x700")
    login_win.configure(bg="#1E1E2F")
    login_win.resizable(False, False)

    # Header Frame
    header_frame = tk.Frame(login_win, bg="#2A2A3F", height=120)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)

    tk.Label(
        header_frame, 
        text="🏥",
        font=("Segoe UI", 50),
        bg="#2A2A3F",
        fg="#FFFFFF"
    ).pack(pady=(20, 5))

    tk.Label(
        header_frame, 
        text="Diabetes AI Predictor",
        font=("Segoe UI", 16, "bold"),
        bg="#2A2A3F",
        fg="#AAAAAA"
    ).pack()

    # Main Content Frame
    content_frame = tk.Frame(login_win, bg="#1E1E2F")
    content_frame.pack(fill="both", expand=True, padx=50, pady=30)

    tk.Label(
        content_frame, 
        text="Welcome Back!",
        font=("Segoe UI", 28, "bold"),
        fg="#FFFFFF",
        bg="#1E1E2F"
    ).pack(pady=(0, 10))

    tk.Label(
        content_frame, 
        text="Sign in to continue",
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
    username_frame.pack(fill="x", pady=(0, 20))

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
    password_frame.pack(fill="x", pady=(0, 30))

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
    entry_password.bind('<Return>', lambda e: login_user())

    # Login Button
    login_button = tk.Button(
        content_frame,
        text="Login",
        font=("Segoe UI", 16, "bold"),
        bg="#5A5AFF",
        fg="#FFFFFF",
        command=login_user,
        relief="flat",
        cursor="hand2",
        activebackground="#6B6BFF",
        activeforeground="#FFFFFF",
        bd=0,
        padx=20,
        pady=15
    )
    login_button.pack(fill="x", pady=(0, 20))
    login_button.bind("<Enter>", on_enter)
    login_button.bind("<Leave>", on_leave)

    # Divider
    divider_frame = tk.Frame(content_frame, bg="#1E1E2F")
    divider_frame.pack(fill="x", pady=15)

    tk.Frame(divider_frame, bg="#3A3A4F", height=1).pack(side="left", fill="x", expand=True)
    tk.Label(divider_frame, text="OR", font=("Segoe UI", 10), bg="#1E1E2F", fg="#AAAAAA", padx=10).pack(side="left")
    tk.Frame(divider_frame, bg="#3A3A4F", height=1).pack(side="left", fill="x", expand=True)

    # Create Account Button
    def on_register_enter(e):
        e.widget['background'] = '#3A3A4F'

    def on_register_leave(e):
        e.widget['background'] = '#2E2E3F'

    def open_register():
        login_win.destroy()
        open_register_window()

    register_button = tk.Button(
        content_frame,
        text="📝 Create New Account",
        font=("Segoe UI", 14, "bold"),
        bg="#2E2E3F",
        fg="#FFFFFF",
        relief="flat",
        cursor="hand2",
        command=open_register,
        activebackground="#3A3A4F",
        activeforeground="#FFFFFF",
        bd=0,
        padx=20,
        pady=12
    )
    register_button.pack(fill="x", pady=(10, 0))
    register_button.bind("<Enter>", on_register_enter)
    register_button.bind("<Leave>", on_register_leave)

    # Text below button
    tk.Label(
        content_frame,
        text="Join us and start monitoring your health!",
        font=("Segoe UI", 10, "italic"),
        bg="#1E1E2F",
        fg="#888888"
    ).pack(pady=(10, 0))

    # Footer
    footer = tk.Frame(login_win, bg="#2A2A3F", height=50)
    footer.pack(fill="x", side="bottom")
    footer.pack_propagate(False)

    tk.Label(
        footer,
        text="© 2024 Diabetes AI - Powered by Machine Learning",
        font=("Segoe UI", 9),
        bg="#2A2A3F",
        fg="#666666"
    ).pack(pady=15)

    login_win.mainloop()


if __name__ == "__main__":
    open_login_window()