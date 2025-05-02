import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import io
import geocoder
from datetime import datetime



# ====== Configuration ======
API_KEY = "ef30f5b0aa7ea8b45fa3f9a5bda6cfc0"  #  OpenWeatherMap API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct"
ONECALL_URL = "https://api.openweathermap.org/data/3.0/onecall"


# ====== Weather App Class ======
class WeatherApp:
    
    def detect_location(self):
      try:
        g = geocoder.ip('me')
        city = g.city
        if city:
            self.city_entry.delete(0, tk.END)
            self.city_entry.insert(0, city)
            self.get_weather()
        else:
            messagebox.showwarning("Location Error", "Could not detect your location.")
      except Exception as e:
        messagebox.showerror("Error", f"Location detection failed: {e}")
    
    def toggle_theme(self):
     self.current_theme = "dark" if self.current_theme == "light" else "light"
     self.apply_theme()


    def __init__(self, root):
        self.current_theme = "light"
        self.themes = {
    "light": {
        "bg": "#f0f4f7",
        "fg": "#000000",
        "entry_bg": "#ffffff",
        "button_bg": "#e0e0e0"
    },
    "dark": {
        "bg": "#1e1e1e",
        "fg": "#ffffff",
        "entry_bg": "#2d2d2d",
        "button_bg": "#444444"
    }
    }

        self.root = root
        self.root.title("Weather App")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f4f7")

        self.setup_ui()
    
    def apply_theme(self):
     theme = self.themes[self.current_theme]
     self.root.configure(bg=theme["bg"])
     self.title_label.configure(bg=theme["bg"], fg=theme["fg"])
     self.city_entry.configure(bg=theme["entry_bg"], fg=theme["fg"], insertbackground=theme["fg"])
     self.result_label.configure(bg=theme["bg"], fg=theme["fg"])
     self.icon_label.configure(bg=theme["bg"])
    
     for btn in self.buttons:
        btn.configure(bg=theme["button_bg"], fg=theme["fg"], activebackground=theme["entry_bg"])



    def setup_ui(self): # making setup_ui() aware for Theme Awareness
        self.title_label = tk.Label(self.root, text="Weather Forecast", font=("Helvetica", 18, "bold"))
        self.title_label.pack(pady=20)

        self.city_entry = tk.Entry(self.root, font=("Helvetica", 14), width=25, justify="center")
        self.city_entry.pack(pady=10)

        self.buttons = []

        detect_button = tk.Button(self.root, text="Detect My Location", font=("Helvetica", 11), command=self.detect_location)
        detect_button.pack(pady=5)
        self.buttons.append(detect_button)

        # check_button = tk.Button(self.root, text="Check Weather", font=("Helvetica", 12), command=self.get_weather)
        # check_button.pack(pady=5)
        # self.buttons.append(check_button)

        theme_button = tk.Button(self.root, text="Toggle Theme", font=("Helvetica", 11), command=self.toggle_theme)
        theme_button.pack(pady=5)
        self.buttons.append(theme_button)

        tk.Button(self.root, text="Check Weather", font=("Helvetica", 12), command=self.get_weather).pack(pady=10)

        self.icon_label = tk.Label(self.root, bg="#f0f4f7")
        self.icon_label.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 12), bg="#f0f4f7", justify="left", wraplength=350)
        self.result_label.pack(pady=10)

        tk.Button(self.root, text="Detect My Location", font=("Helvetica", 11), command=self.detect_location).pack(pady=5)
        

        self.apply_theme()

    # Adding Method to Get Lat/Lon from City
    def get_coordinates(self, city):
     try:
        params = {
            'q': city,
            'appid': API_KEY,
            'limit': 1
        }
        response = requests.get(GEOCODE_URL, params=params)
        data = response.json()
        if data:
            lat = data[0]['lat']
            lon = data[0]['lon']
            return lat, lon
        else:
            return None, None
     except:
        return None, None
     
    def get_forecast(self, lat, lon):
       try:
        params = {
            'lat': lat,
            'lon': lon,
            'appid': API_KEY,
            'units': 'metric',
            'exclude': 'minutely,hourly,alerts,current'
        }
        response = requests.get(ONECALL_URL, params=params)
        data = response.json()

        forecast_text = "\n\n3-Day Forecast:\n"
        for i in range(1, 4):
            day = data['daily'][i]
            date = datetime.fromtimestamp(day['dt']).strftime('%A')
            desc = day['weather'][0]['description'].title()
            temp = day['temp']['day']
            forecast_text += f"{date}: {temp:.1f}°C, {desc}\n"
        return forecast_text
       except Exception as e:
        return "\nCould not retrieve forecast."



    def get_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Required", "Please enter a city name.")
            return

        try:
            url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                weather = data["weather"][0]
                main = data["main"]
                wind = data["wind"]

                description = weather["description"].title()
                icon_code = weather["icon"]
                temp = main["temp"]
                humidity = main["humidity"]
                pressure = main["pressure"]
                wind_speed = wind["speed"]

                self.show_icon(icon_code)

                weather_info = (
                    f"City: {city.title()}\n"
                    f"Temperature: {temp} °C\n"
                    f"Weather: {description}\n"
                    f"Humidity: {humidity}%\n"
                    f"Pressure: {pressure} hPa\n"
                    f"Wind Speed: {wind_speed} m/s"
                )
                self.result_label.config(text=weather_info)
            else:
                self.result_label.config(text="City not found. Please try again.")
                self.icon_label.config(image='')

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

            

    def show_icon(self, icon_code):
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_data = requests.get(icon_url).content
        icon_image = Image.open(io.BytesIO(icon_data))
        icon_photo = ImageTk.PhotoImage(icon_image)

        self.icon_label.config(image=icon_photo)
        self.icon_label.image = icon_photo  # Keep a reference

# ====== Main Application ======
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
