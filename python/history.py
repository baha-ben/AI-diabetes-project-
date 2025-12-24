import tkinter as tk
from tkinter import ttk
import mysql.connector
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def open_history_page(user_id):

    # DATABASE
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="diabetes_app"
    )
    cursor = conn.cursor()

    cursor.execute(
        "SELECT date, glucose, bmi, age, result FROM diabetes_data WHERE user_id=%s ORDER BY date DESC",
        (user_id,)
    )
    records = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM diabetes_data WHERE user_id=%s", (user_id,))
    total_tests = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM diabetes_data WHERE user_id=%s AND result='Diabetic'",
        (user_id,)
    )
    diabetic = cursor.fetchone()[0]
    non_diabetic = total_tests - diabetic
    conn.close()

    # WINDOW 
    window = tk.Toplevel()
    window.title("Health History Dashboard")
    window.geometry("1000x700")
    window.configure(bg="#1E1E2F")
    window.resizable(True, True)

    # HEADER 
    header_frame = tk.Frame(window, bg="#2A2A3F", height=80)
    header_frame.pack(fill="x", side="top")
    header_frame.pack_propagate(False)

    tk.Label(
        header_frame,
        text="📊 Health History Dashboard",
        font=("Segoe UI", 28, "bold"),
        bg="#2A2A3F",
        fg="#FFFFFF"
    ).pack(pady=20)

    # MAIN CONTAINER
    main_container = tk.Frame(window, bg="#1E1E2F")
    main_container.pack(fill="both", expand=True, padx=20, pady=20)

    # STATS CARDS
    stats_frame = tk.Frame(main_container, bg="#1E1E2F")
    stats_frame.pack(fill="x", pady=(0, 20))

    stats = [
        ("📋 Total Tests", total_tests, "#5A5AFF", "#4848CC"),
        ("❌ Diabetic", diabetic, "#FF4C4C", "#CC3A3A"),
        ("✅ Not Diabetic", non_diabetic, "#4CFF88", "#3ACC6B")
    ]

    for i, (title, value, bg_color, border_color) in enumerate(stats):
        card = tk.Frame(stats_frame, bg=bg_color, highlightbackground=border_color, highlightthickness=3)
        card.pack(side="left", expand=True, padx=15, pady=10, fill="both")
        
        card_inner = tk.Frame(card, bg=bg_color)
        card_inner.pack(expand=True, padx=15, pady=15)

        tk.Label(
            card_inner, 
            text=title, 
            font=("Segoe UI", 14, "bold"),
            bg=bg_color, 
            fg="white"
        ).pack(pady=(5, 10))
        
        tk.Label(
            card_inner, 
            text=str(value), 
            font=("Segoe UI", 36, "bold"),
            bg=bg_color, 
            fg="white"
        ).pack()

    # CONTENT AREA WITH SCROLL 
    content_frame = tk.Frame(main_container, bg="#1E1E2F")
    content_frame.pack(fill="both", expand=True)

    # Create Canvas with Scrollbar
    canvas = tk.Canvas(content_frame, bg="#1E1E2F", highlightthickness=0)
    scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#1E1E2F")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Mouse wheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # TWO COLUMN LAYOUT 
    left_column = tk.Frame(scrollable_frame, bg="#1E1E2F")
    left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))

    right_column = tk.Frame(scrollable_frame, bg="#1E1E2F")
    right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))

    # TABLE (LEFT COLUMN) 
    table_container = tk.Frame(left_column, bg="#2A2A3F", highlightbackground="#3A3A4F", highlightthickness=2)
    table_container.pack(fill="both", expand=True, pady=10)

    tk.Label(
        table_container,
        text="📝 Recent Tests",
        font=("Segoe UI", 18, "bold"),
        bg="#2A2A3F",
        fg="white"
    ).pack(pady=15, padx=20, anchor="w")

    # Table Header with Grid Layout
    header_frame = tk.Frame(table_container, bg="#3A3A4F")
    header_frame.pack(fill="x", padx=20, pady=(0, 5))

    headers = ["📅 Date", "🩸 Glucose", "⚖️ BMI", "👤 Age", "🏥 Result"]
    col_widths = [20, 15, 12, 10, 18]  # Custom widths for each column
    
    for i, (h, width) in enumerate(zip(headers, col_widths)):
        header_cell = tk.Label(
            header_frame, 
            text=h, 
            font=("Segoe UI", 11, "bold"),
            bg="#3A3A4F", 
            fg="white",
            anchor="center",
            padx=10,
            pady=12
        )
        header_cell.grid(row=0, column=i, sticky="ew", padx=2)
        header_frame.grid_columnconfigure(i, weight=1, minsize=width*6)

    # Table Rows with Grid Layout
    table_scroll_frame = tk.Frame(table_container, bg="#2A2A3F")
    table_scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))

    for idx, record in enumerate(records[:10]):  # Show last 10 records
        row_bg = "#252535" if idx % 2 == 0 else "#2A2A3F"
        
        row_frame = tk.Frame(table_scroll_frame, bg=row_bg)
        row_frame.pack(fill="x", pady=1)

        for i, value in enumerate(record):
            # Format date
            if i == 0:
                value = str(value).split()[0]  # Show only date part
            
            # Format decimal numbers
            if i in [1, 2] and isinstance(value, (int, float)):
                value = f"{float(value):.1f}"
            
            # Color result column
            if i == 4:
                fg_color = "#FF4C4C" if value == "Diabetic" else "#4CFF88"
                font_weight = "bold"
            else:
                fg_color = "white"
                font_weight = "normal"
            
            cell = tk.Label(
                row_frame, 
                text=str(value), 
                font=("Segoe UI", 10, font_weight),
                bg=row_bg, 
                fg=fg_color,
                anchor="center",
                padx=10,
                pady=10
            )
            cell.grid(row=0, column=i, sticky="ew", padx=2)
            row_frame.grid_columnconfigure(i, weight=1, minsize=col_widths[i]*6)

    # CHART (RIGHT COLUMN) 
    chart_container = tk.Frame(right_column, bg="#2A2A3F", highlightbackground="#3A3A4F", highlightthickness=2)
    chart_container.pack(fill="both", expand=True, pady=10)

    tk.Label(
        chart_container,
        text="📈 Results Distribution",
        font=("Segoe UI", 18, "bold"),
        bg="#2A2A3F",
        fg="white"
    ).pack(pady=15, padx=20, anchor="w")

    fig = Figure(figsize=(5, 5), dpi=100, facecolor="#2A2A3F")
    ax = fig.add_subplot(111)
    ax.set_facecolor("#2A2A3F")
    
    colors = ['#FF4C4C', '#4CFF88']
    bars = ax.bar(["Diabetic", "Not Diabetic"], [diabetic, non_diabetic], color=colors, width=0.6, edgecolor='white', linewidth=2)
    
    ax.set_ylabel("Number of Tests", color='white', fontsize=12, fontweight='bold')
    ax.set_title("Health Status Overview", color='white', fontsize=14, fontweight='bold', pad=20)
    ax.tick_params(colors='white', labelsize=10)
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3, color='white', linestyle='--')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', color='white', fontweight='bold', fontsize=12)

    chart_canvas = FigureCanvasTkAgg(fig, master=chart_container)
    chart_canvas.draw()
    chart_canvas.get_tk_widget().pack(expand=True, fill="both", padx=20, pady=(0, 20))

    #  FOOTER 
    footer = tk.Frame(window, bg="#2A2A3F", height=50)
    footer.pack(fill="x", side="bottom")
    footer.pack_propagate(False)

    tk.Label(
        footer,
        text="💡 Stay healthy and monitor your health regularly",
        font=("Segoe UI", 11, "italic"),
        bg="#2A2A3F",
        fg="#AAAAAA"
    ).pack(pady=12)

    window.mainloop()