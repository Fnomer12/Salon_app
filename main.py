import tkinter as tk
from tkinter import ttk, messagebox, Canvas
from tkcalendar import Calendar
from PIL import Image, ImageTk
from datetime import datetime
import mysql.connector

# Background image path
wallpaper_path = "/Users/macbookpro/Desktop/School/Year 2 Semester 1/Procedural Programming/Salon Management System/myenv/Pic.jpeg"

# Styles
male_styles = [
    ("Buzz Cut", 30), ("Fade", 40), ("Pompadour", 50),
    ("Crew Cut", 35), ("Quiff", 45), ("Undercut", 40),
    ("Comb Over", 50), ("Flat Top", 38), ("French Crop", 42),
    ("Caesar Cut", 33)
]

female_styles = [
    ("Box Braids", 120), ("Cornrows", 100), ("Twists", 110),
    ("Sew-in Weave", 150), ("Crochet Braids", 130), ("Lace Wig", 200),
    ("Silk Press", 90), ("Relaxed Hair", 85), ("Afro Styling", 95),
    ("Faux Locs", 140), ("Bantu Knots", 75), ("Marley Twists", 125),
    ("Knotless Braids", 135), ("Updo", 100), ("Natural Wash & Go", 80),
    ("Flat Twists", 105), ("Passion Twists", 130), ("Halo Braid", 115),
    ("French Braid", 85), ("Dutch Braid", 85), ("Ghana Braids", 120),
    ("Goddess Locs", 160), ("Boho Braids", 140), ("Finger Coils", 90),
    ("Bob Cut", 100), ("Layered Hair", 110), ("Pixie Cut", 95),
    ("High Ponytail", 105), ("Low Bun", 95), ("Side Swept Curls", 115)
]

# MySQL Connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Salon_Management"
    )

def save_booking(user, style_name, price, date_obj, payment_method):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Bookings (name, phone, email, style, price, date, payment_method)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (user["name"], user["phone"], user["email"], style_name, price, date_obj, payment_method))
    conn.commit()
    conn.close()

def open_calendar(user, style, price):
    cal_win = tk.Toplevel()
    cal_win.title("Select Booking Date")
    tk.Label(cal_win, text="Pick a date for your appointment:", font=("Helvetica", 12)).pack(pady=10)

    current_date = datetime.now().date()
    cal = Calendar(cal_win, selectmode='day', mindate=current_date)
    cal.pack(pady=10)

    def confirm_date():
        date = cal.get_date()
        open_payment_method(user, style, price, date)
        cal_win.destroy()

    ttk.Button(cal_win, text="Confirm Date", command=confirm_date).pack(pady=10)

def open_payment_method(user, style_name, price, date):
    payment_win = tk.Toplevel()
    payment_win.title("Select Payment Method")
    payment_win.geometry("400x300")

    tk.Label(payment_win, text="Choose a Payment Method", font=("Helvetica", 14)).pack(pady=20)
    
    ttk.Button(payment_win, text="Credit Card 💳", command=lambda: process_payment(user, style_name, price, date, "Credit Card")).pack(pady=10)
    ttk.Button(payment_win, text="PayPal 💻", command=lambda: process_payment(user, style_name, price, date, "PayPal")).pack(pady=10)
    ttk.Button(payment_win, text="Cash 💵", command=lambda: process_payment(user, style_name, price, date, "Cash")).pack(pady=10)

def process_payment(user, style_name, price, date, payment_method):
    try:
        # Convert string date to datetime object
        date_obj = datetime.strptime(date, "%m/%d/%y").date()

        # Save to DB
        save_booking(user, style_name, price, date_obj, payment_method)

        # Format date for receipt (DD-MM-YYYY)
        formatted_date = date_obj.strftime("%d-%m-%Y")

        receipt = (
            f"Receipt:\n\n"
            f"Name: {user['name']}\n"
            f"Style: {style_name}\n"
            f"Price: US ${price}\n"
            f"Date: {formatted_date}\n"
            f"Payment Method: {payment_method}"
        )
        messagebox.showinfo("Booking Successful", receipt)

    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_styles(user, styles, gender):
    style_window = tk.Toplevel()
    style_window.title(f"{gender} Styles")
    style_window.geometry("600x600")

    tk.Label(style_window, text=f"{gender} Styles - Choose Your Look", font=("Helvetica", 16, "bold")).pack(pady=10)

    canvas = tk.Canvas(style_window)
    scrollbar = ttk.Scrollbar(style_window, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    for name, price in styles:
        frame = tk.Frame(scroll_frame, pady=5)
        tk.Label(frame, text=f"{name} - US ${price}", font=("Helvetica", 12)).pack(side="left", padx=10)
        ttk.Button(frame, text="Book", command=lambda n=name, p=price: open_calendar(user, n, p)).pack(side="right")
        frame.pack(fill="x", padx=20)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

def open_selection_page(name, phone, email):
    if not name or not phone or not email:
        messagebox.showerror("Error", "All fields must be filled out.")
        return

    user = {"name": name, "phone": phone, "email": email}
    win = tk.Toplevel()
    win.title("Selection Page")
    win.geometry("400x300")

    tk.Label(win, text=f"Welcome {name}!", font=("Helvetica", 16)).pack(pady=20)
    ttk.Button(win, text="Male Section 💇‍♂️", width=30, command=lambda: show_styles(user, male_styles, "Male")).pack(pady=10)
    ttk.Button(win, text="Female Section 💇‍♀️", width=30, command=lambda: show_styles(user, female_styles, "Female")).pack(pady=10)

# GUI setup
root = tk.Tk()
root.title("BOTERO SALON - Booking")
root.geometry("500x500")

# Background image
try:
    bg_img = Image.open(wallpaper_path).resize((500, 500))
    bg_photo = ImageTk.PhotoImage(bg_img)

    canvas = Canvas(root, width=500, height=500)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
except:
    canvas = Canvas(root, width=500, height=500)
    canvas.pack(fill="both", expand=True)

# Login Form
canvas.create_text(250, 40, text="Botero Login", font=("Helvetica", 16, "bold"), fill="white")
canvas.create_text(250, 90, text="Name", fill="white", font=("Helvetica", 12))
entry_name = tk.Entry(root)
canvas.create_window(250, 110, window=entry_name)

canvas.create_text(250, 150, text="Phone", fill="white", font=("Helvetica", 12))
entry_phone = tk.Entry(root)
canvas.create_window(250, 170, window=entry_phone)

canvas.create_text(250, 210, text="Email", fill="white", font=("Helvetica", 12))
entry_email = tk.Entry(root)
canvas.create_window(250, 230, window=entry_email)

proceed_button = ttk.Button(root, text="Proceed", command=lambda: open_selection_page(entry_name.get(), entry_phone.get(), entry_email.get()))
canvas.create_window(250, 280, window=proceed_button)

root.mainloop()



























