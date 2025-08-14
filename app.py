import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from datetime import datetime

API_KEY = "39f60aa25fc2c46f00a018ec05c0aac6"  # Replace with your OpenWeatherMap API key

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=39f60aa25fc2c46f00a018ec05c0aac6&units=metric"
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid=39f60aa25fc2c46f00a018ec05c0aac6   &units=metric"
    
    try:
        weather_data = requests.get(url).json()
        forecast_data = requests.get(forecast_url).json()
        
        if weather_data.get("cod") != 200:
            raise ValueError("City not found")

        temp = weather_data['main']['temp']
        weather = weather_data['weather'][0]['main']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        date = datetime.now().strftime("%a, %d %b")

        # Update main UI
        city_label.config(text=city.title())
        date_label.config(text=date)
        temp_label.config(text=f"{int(temp)}°C")
        weather_label.config(text=weather)
        humidity_label.config(text=f"Humidity\n{humidity}%")
        wind_label.config(text=f"Wind Speed\n{wind_speed} m/s")

        # Forecast (next 3 days every 24 hours from current)
        for i in range(1, 4):
            day_data = forecast_data['list'][i * 8]  # Approx every 24 hours
            date_txt = datetime.strptime(day_data['dt_txt'], "%Y-%m-%d %H:%M:%S")
            day_label[i-1].config(text=date_txt.strftime("%b %d"))
            icon = day_data['weather'][0]['main']
            temp_val = int(day_data['main']['temp'])
            icon_label[i-1].config(text=icon)
            temp_forecast_label[i-1].config(text=f"{temp_val}°C")
    
    except Exception as e:
        city_label.config(text="City not found")
        print("Error:", e)

# GUI Setup
root = tk.Tk()
root.title("Weather App")
root.geometry("400x600")
root.configure(bg="#d1e0e0")

# Rounded frame
frame = tk.Frame(root, bg="#e6f2ff", bd=2, relief="groove")
frame.place(relx=0.5, rely=0.5, anchor="center", width=320, height=500)

# Search
search_var = tk.StringVar()
search_entry = tk.Entry(frame, textvariable=search_var, font=("Arial", 12), width=22)
search_entry.place(x=20, y=20)

search_btn = tk.Button(frame, text="🔍", command=lambda: get_weather(search_var.get()))
search_btn.place(x=250, y=18)

# City and Date
city_label = tk.Label(frame, text="City", font=("Arial", 14), bg="#e6f2ff")
city_label.place(x=20, y=60)

date_label = tk.Label(frame, text="Date", font=("Arial", 10), bg="#e6f2ff")
date_label.place(x=200, y=65)

# Weather Main Info
temp_label = tk.Label(frame, text="0°C", font=("Arial", 28, "bold"), bg="#e6f2ff")
temp_label.place(x=110, y=110)

weather_label = tk.Label(frame, text="Clouds", font=("Arial", 12), bg="#e6f2ff")
weather_label.place(x=120, y=160)

# Humidity and Wind
humidity_label = tk.Label(frame, text="Humidity\n%", font=("Arial", 10), bg="#e6f2ff", justify="center")
humidity_label.place(x=50, y=200)

wind_label = tk.Label(frame, text="Wind\nSpeed", font=("Arial", 10), bg="#e6f2ff", justify="center")
wind_label.place(x=200, y=200)

# Forecast
forecast_frame = tk.Frame(frame, bg="#cce6ff")
forecast_frame.place(x=20, y=270, width=280, height=120)

day_label = []
icon_label = []
temp_forecast_label = []

for i in range(3):
    f = tk.Frame(forecast_frame, bg="#ffffff", relief="ridge", bd=1)
    f.place(x=10 + i*90, y=10, width=80, height=90)

    d = tk.Label(f, text="Day", font=("Arial", 9), bg="#ffffff")
    d.pack(pady=2)
    day_label.append(d)

    icon = tk.Label(f, text="☁️", font=("Arial", 12), bg="#ffffff")
    icon.pack()
    icon_label.append(icon)

    t = tk.Label(f, text="°C", font=("Arial", 10), bg="#ffffff")
    t.pack()
    temp_forecast_label.append(t)

root.mainloop()
