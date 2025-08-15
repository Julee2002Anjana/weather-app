import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from datetime import datetime

API_KEY = "39f60aa25fc2c46f00a018ec05c0aac6"

# ---------------- Weather icons for day and night ----------------
ICON_MAP = {
    "clear sky": {"day": "icons/01.png", "night": "icons/10.png"},
    "few clouds": {"day": "icons/02.png", "night": "icons/11.png"},
    "scattered clouds": {"day": "icons/07.png", "night": "icons/15.png"},
    "broken clouds": {"day": "icons/08.png", "night": "icons/16.png"},
    "shower rain": {"day": "icons/09.png", "night": "icons/14.png"},
    "rain": {"day": "icons/06.png", "night": "icons/06.png"},
    "thunderstorm": {"day": "icons/03.png", "night": "icons/13.png"},
    "mist": {"day": "icons/05.png", "night": "icons/17.png"}
}

def get_icon_path(description, current_time, sunrise, sunset):
    desc = description.lower()
    is_daytime = sunrise <= current_time <= sunset
    for key in ICON_MAP:
        if key in desc:
            return ICON_MAP[key]["day"] if is_daytime else ICON_MAP[key]["night"]
    return ICON_MAP["clear sky"]["day"] if is_daytime else ICON_MAP["clear sky"]["night"]

# ---------------- Weather Fetch ----------------
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    try:
        weather_data = requests.get(url).json()
        forecast_data = requests.get(forecast_url).json()

        if weather_data.get("cod") != 200:
            raise ValueError("City not found")

        temp = weather_data['main']['temp']
        weather_desc = weather_data['weather'][0]['description']
        weather = weather_desc.title()
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        date = datetime.now().strftime("%A, %d %B %Y")

        current_time = weather_data['dt']
        sunrise = weather_data['sys']['sunrise']
        sunset = weather_data['sys']['sunset']

        city_label.config(text=city.title())
        date_label.config(text=date)
        temp_label.config(text=f"{int(temp)}°C")
        weather_label.config(text=weather)
        humidity_label.config(text=f"💧 {humidity}%")
        wind_label.config(text=f"🌬 {wind_speed} m/s")

        icon_path = get_icon_path(weather_desc, current_time, sunrise, sunset)
        icon_img = Image.open(icon_path).resize((150, 150), Image.LANCZOS)
        icon_photo = ImageTk.PhotoImage(icon_img)
        main_icon_label.config(image=icon_photo)
        main_icon_label.image = icon_photo

        for i in range(1, 4):
            day_data = forecast_data['list'][i * 8]
            date_txt = datetime.strptime(day_data['dt_txt'], "%Y-%m-%d %H:%M:%S")
            day_label[i-1].config(text=date_txt.strftime("%b %d"))

            forecast_desc = day_data['weather'][0]['description']
            forecast_icon_path = get_icon_path(forecast_desc, day_data['dt'], sunrise, sunset)
            forecast_icon_img = Image.open(forecast_icon_path).resize((80, 80), Image.LANCZOS)
            forecast_icon_photo = ImageTk.PhotoImage(forecast_icon_img)
            icon_label[i-1].config(image=forecast_icon_photo)
            icon_label[i-1].image = forecast_icon_photo

            temp_forecast_label[i-1].config(text=f"{int(day_data['main']['temp'])}°C")

    except Exception as e:
        messagebox.showerror("Error", f"Could not get weather: {e}")

def resize_bg(event):
    new_width = event.width
    new_height = event.height
    resized = bg_img.resize((new_width, new_height), Image.LANCZOS)
    bg_photo_resized = ImageTk.PhotoImage(resized)
    bg_label.config(image=bg_photo_resized)
    bg_label.image = bg_photo_resized  

# ----------------- Root -----------------
root = tk.Tk()
root.title("Weather App")
root.geometry("480x720")

# Load background image
bg_img = Image.open("background.jpg")
bg_photo = ImageTk.PhotoImage(bg_img)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
root.bind("<Configure>", resize_bg)

# ---------------- Rounded Main Frame ----------------
frame_canvas = tk.Canvas(root, bg="white", highlightthickness=0)

frame_canvas.place(relx=0.5, rely=0.5, anchor="center", width=420, height=660)

r = 30  # corner radius
x0, y0, x1, y1 = 0, 0, 420, 660
frame_canvas.create_arc((x0, y0, x0 + 2*r, y0 + 2*r), start=90, extent=90, fill="#ffffff", outline="#ffffff")
frame_canvas.create_arc((x1 - 2*r, y0, x1, y0 + 2*r), start=0, extent=90, fill="#ffffff", outline="#ffffff")
frame_canvas.create_arc((x0, y1 - 2*r, x0 + 2*r, y1), start=180, extent=90, fill="#ffffff", outline="#ffffff")
frame_canvas.create_arc((x1 - 2*r, y1 - 2*r, x1, y1), start=270, extent=90, fill="#ffffff", outline="#ffffff")
frame_canvas.create_rectangle((r, 0, x1 - r, y1), fill="#ffffff", outline="#ffffff")
frame_canvas.create_rectangle((0, r, x1, y1 - r), fill="#ffffff", outline="#ffffff")

# Inner frame for widgets
frame = tk.Frame(frame_canvas, bg="#ffffff", bd=0)
frame.place(x=0, y=0, width=420, height=660)

# ---------------- Advanced Search Bar ----------------
search_var = tk.StringVar()
search_canvas = tk.Canvas(frame, bg="#ffffff", highlightthickness=0)
search_canvas.place(x=20, y=20, width=380, height=50)

r = 25
search_canvas.create_arc((0,0,2*r,2*r), start=90, extent=90, fill="#f9f9f9", outline="#f9f9f9")
search_canvas.create_arc((380-2*r,0,380,2*r), start=0, extent=90, fill="#f9f9f9", outline="#f9f9f9")
search_canvas.create_arc((0,55-2*r,2*r,55), start=180, extent=90, fill="#f9f9f9", outline="#f9f9f9")
search_canvas.create_arc((380-2*r,55-2*r,380,55), start=270, extent=90, fill="#f9f9f9", outline="#f9f9f9")
search_canvas.create_rectangle((r, 0, 380-r, 55), fill="#f9f9f9", outline="#f9f9f9")
search_canvas.create_rectangle((0, r, 380, 55-r), fill="#f9f9f9", outline="#f9f9f9")

search_entry = tk.Entry(frame, textvariable=search_var, font=("Arial", 14),
                        bg="#f9f9f9", fg="#2d2d2d", bd=0)
search_entry.place(x=60, y=25, width=250, height=30)

placeholder_text = "Enter city name..."
search_entry.insert(0, placeholder_text)
search_entry.config(fg="grey")

def clear_placeholder(event):
    if search_entry.get() == placeholder_text:
        search_entry.delete(0, tk.END)
        search_entry.config(fg="#2d2d2d")

def add_placeholder(event):
    if search_entry.get() == "":
        search_entry.insert(0, placeholder_text)
        search_entry.config(fg="grey")

search_entry.bind("<FocusIn>", clear_placeholder)
search_entry.bind("<FocusOut>", add_placeholder)

search_img = Image.open("icons/search.png").resize((25, 25), Image.LANCZOS)
search_photo = ImageTk.PhotoImage(search_img)
search_icon = tk.Button(frame, image=search_photo, bg="#f9f9f9", bd=0, relief="flat",
                        cursor="hand2", command=lambda: get_weather(search_var.get()))
search_icon.image = search_photo
search_icon.place(x=320, y=27, width=25, height=25)

# ---------------- City and Date ----------------
city_label = tk.Label(frame, text="City", font=("Arial", 22, "bold"), bg="#ffffff", fg="#2d2d2d")
city_label.place(x=20, y=80)

date_label = tk.Label(frame, text="Date", font=("Arial", 14), bg="#ffffff", fg="#555555")
date_label.place(x=20, y=120)

# ---------------- Main Weather Icon & Info ----------------
main_icon_label = tk.Label(frame, bg="#ffffff")
main_icon_label.place(x=130, y=150)

temp_label = tk.Label(frame, text="0°C", font=("Arial", 46, "bold"), bg="#ffffff", fg="#2d2d2d")
temp_label.place(x=140, y=300)

weather_label = tk.Label(frame, text="Clear", font=("Arial", 17), bg="#ffffff", fg="#555555")
weather_label.place(x=130, y=380)

humidity_label = tk.Label(frame, text="💧 --%", font=("Arial", 16), bg="#ffffff", fg="#2d2d2d")
humidity_label.place(x=60, y=415)

wind_label = tk.Label(frame, text="🌬 -- m/s", font=("Arial", 16), bg="#ffffff", fg="#2d2d2d")
wind_label.place(x=220, y=415)

# ---------------- Forecast Section ----------------
forecast_title = tk.Label(frame, text="3-Day Forecast", font=("Arial", 16, "bold"), bg="#ffffff", fg="#2d2d2d")
forecast_title.place(x=120, y=470)

forecast_frame = tk.Frame(frame, bg="#e8e8e8")
forecast_frame.place(x=20, y=510, width=380, height=140)

day_label, icon_label, temp_forecast_label = [], [], []
for i in range(3):
    f = tk.Frame(forecast_frame, bg="#ffffff")
    f.place(x=15 + i * 120, y=10, width=110, height=120)

    d = tk.Label(f, text="Day", font=("Arial", 12, "bold"), bg="#ffffff", fg="#2d2d2d")
    d.pack(pady=4)
    day_label.append(d)

    icon = tk.Label(f, bg="#ffffff")
    icon.pack(pady=4)
    icon_label.append(icon)

    t = tk.Label(f, text="°C", font=("Arial", 14, "bold"), bg="#ffffff", fg="#2d2d2d")
    t.pack()
    temp_forecast_label.append(t)

root.mainloop()
