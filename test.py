import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from datetime import datetime

API_KEY = "39f60aa25fc2c46f00a018ec05c0aac6"

# Weather description to icon mapping
ICON_MAP = {
    "clear sky": "icons/01.png",
    "few clouds": "icons/02.png",
    "scattered clouds": "icons/07.png",
    "broken clouds": "icons/08.png",
    "shower rain": "icons/09.png",
    "rain": "icons/06.png",
    "thunderstorm": "icons/03.png",
    "mist": "icons/05.png"
}

def get_icon_path(description):
    """
    Finds the correct local icon for a weather description.
    Uses partial matching to handle cases like 'light rain', 'overcast clouds'.
    """
    desc = description.lower()
    for key in ICON_MAP:
        if key in desc:  # partial match
            return ICON_MAP[key]
    return "icons/01.png"  # default icon if nothing matches

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

        city_label.config(text=city.title())
        date_label.config(text=date)
        temp_label.config(text=f"{int(temp)}°C")
        weather_label.config(text=weather)
        humidity_label.config(text=f"💧 {humidity}%")
        wind_label.config(text=f"🌬 {wind_speed} m/s")

        # Main icon (local image)
        icon_path = get_icon_path(weather_desc)
        icon_img = Image.open(icon_path).resize((150, 150), Image.LANCZOS)
        icon_photo = ImageTk.PhotoImage(icon_img)
        main_icon_label.config(image=icon_photo)
        main_icon_label.image = icon_photo

        # Forecast (next 3 days)
        for i in range(1, 4):
            day_data = forecast_data['list'][i * 8]
            date_txt = datetime.strptime(day_data['dt_txt'], "%Y-%m-%d %H:%M:%S")
            day_label[i-1].config(text=date_txt.strftime("%b %d"))

            forecast_desc = day_data['weather'][0]['description']
            forecast_icon_path = get_icon_path(forecast_desc)
            forecast_icon_img = Image.open(forecast_icon_path).resize((80, 80), Image.LANCZOS)
            forecast_icon_photo = ImageTk.PhotoImage(forecast_icon_img)
            icon_label[i-1].config(image=forecast_icon_photo)
            icon_label[i-1].image = forecast_icon_photo

            temp_forecast_label[i-1].config(text=f"{int(day_data['main']['temp'])}°C")

    except Exception as e:
        messagebox.showerror("Error", f"Could not get weather: {e}")

# ----------------- UI -----------------
root = tk.Tk()
root.title("Weather App")
root.geometry("420x640")
root.configure(bg="#2b2d42")

frame = tk.Frame(root, bg="#3a3f58", bd=0, relief="flat")
frame.place(relx=0.5, rely=0.5, anchor="center", width=360, height=580)

# ---------------- Search Bar ----------------
search_var = tk.StringVar()

search_canvas = tk.Canvas(frame, bg="#3a3f58", highlightthickness=0)
search_canvas.place(x=20, y=20, width=320, height=40)

r = 20
search_canvas.create_arc((0, 0, r*2, r*2), start=90, extent=90, fill="#edf2f4", outline="#edf2f4")
search_canvas.create_arc((320-r*2, 0, 320, r*2), start=0, extent=90, fill="#edf2f4", outline="#edf2f4")
search_canvas.create_arc((0, 40-r*2, r*2, 40), start=180, extent=90, fill="#edf2f4", outline="#edf2f4")
search_canvas.create_arc((320-r*2, 40-r*2, 320, 40), start=270, extent=90, fill="#edf2f4", outline="#edf2f4")
search_canvas.create_rectangle((r, 0, 320-r, 40), fill="#edf2f4", outline="#edf2f4")
search_canvas.create_rectangle((0, r, 320, 40-r), fill="#edf2f4", outline="#edf2f4")

search_entry = tk.Entry(frame, textvariable=search_var, font=("Arial", 14),
                        bg="#edf2f4", fg="#2b2d42", bd=0)
search_entry.place(x=35, y=23, width=240, height=30)

search_img = Image.open("icons/search.png").resize((30, 30), Image.LANCZOS)
search_photo = ImageTk.PhotoImage(search_img)
search_icon = tk.Button(frame, image=search_photo, bg="#edf2f4", bd=0, relief="flat",
                        cursor="hand2", command=lambda: get_weather(search_var.get()))
search_icon.image = search_photo
search_icon.place(x=280, y=23, width=30, height=30)

# ---------------- City and Date ----------------
city_label = tk.Label(frame, text="City", font=("Arial", 20, "bold"), bg="#3a3f58", fg="white")
city_label.place(x=20, y=70)

date_label = tk.Label(frame, text="Date", font=("Arial", 12), bg="#3a3f58", fg="#dcdcdc")
date_label.place(x=20, y=110)

# ---------------- Main Weather Icon & Info ----------------
main_icon_label = tk.Label(frame, bg="#3a3f58")
main_icon_label.place(x=105, y=130)

temp_label = tk.Label(frame, text="0°C", font=("Arial", 40, "bold"), bg="#3a3f58", fg="white")
temp_label.place(x=130, y=280)

weather_label = tk.Label(frame, text="Clear", font=("Arial", 16), bg="#3a3f58", fg="#e0e0e0")
weather_label.place(x=120, y=340)

humidity_label = tk.Label(frame, text="💧 --%", font=("Arial", 14), bg="#3a3f58", fg="white")
humidity_label.place(x=60, y=380)

wind_label = tk.Label(frame, text="🌬 -- m/s", font=("Arial", 14), bg="#3a3f58", fg="white")
wind_label.place(x=200, y=380)

# ---------------- Forecast Section ----------------
forecast_title = tk.Label(frame, text="3-Day Forecast", font=("Arial", 16, "bold"), bg="#3a3f58", fg="white")
forecast_title.place(x=100, y=430)

forecast_frame = tk.Frame(frame, bg="#8d99ae")
forecast_frame.place(x=20, y=470, width=320, height=100)

day_label, icon_label, temp_forecast_label = [], [], []
for i in range(3):
    f = tk.Frame(forecast_frame, bg="#edf2f4")
    f.place(x=15 + i * 100, y=10, width=90, height=80)

    d = tk.Label(f, text="Day", font=("Arial", 10, "bold"), bg="#edf2f4", fg="#2b2d42")
    d.pack(pady=2)
    day_label.append(d)

    icon = tk.Label(f, bg="#edf2f4")
    icon.pack()
    icon_label.append(icon)

    t = tk.Label(f, text="°C", font=("Arial", 12, "bold"), bg="#edf2f4", fg="#2b2d42")
    t.pack()
    temp_forecast_label.append(t)

root.mainloop()
