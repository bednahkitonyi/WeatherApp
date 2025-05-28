import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import io
import geocoder
from datetime import datetime
from typing import Optional, Tuple, Dict, Any


class WeatherConfig:
    """Configuration constants for the weather app."""
    API_KEY = "ef30f5b0aa7ea8b45fa3f9a5bda6cfc0"
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct"
    ONECALL_URL = "https://api.openweathermap.org/data/3.0/onecall"
    ICON_URL = "http://openweathermap.org/img/wn/{icon_code}@2x.png"


class ThemeManager:
    """Manages application themes."""
    
    THEMES = {
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
    
    def __init__(self, initial_theme: str = "light"):
        self.current_theme = initial_theme
    
    def toggle_theme(self) -> str:
        """Toggle between light and dark themes."""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        return self.current_theme
    
    def get_current_theme(self) -> Dict[str, str]:
        """Get the current theme configuration."""
        return self.THEMES[self.current_theme]


class WeatherAPI:
    """Handles all API interactions."""
    
    @staticmethod
    def get_coordinates(city: str) -> Tuple[Optional[float], Optional[float]]:
        """Get latitude and longitude for a given city."""
        try:
            params = {
                'q': city,
                'appid': WeatherConfig.API_KEY,
                'limit': 1
            }
            response = requests.get(WeatherConfig.GEOCODE_URL, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data:
                return data[0]['lat'], data[0]['lon']
            return None, None
        except Exception:
            return None, None
    
    @staticmethod
    def get_current_weather(city: str) -> Optional[Dict[str, Any]]:
        """Get current weather data for a city."""
        try:
            params = {
                'q': city,
                'appid': WeatherConfig.API_KEY,
                'units': 'metric'
            }
            response = requests.get(WeatherConfig.BASE_URL, params=params)
            response.raise_for_status()
            
            return response.json()
        except Exception:
            return None
    
    @staticmethod
    def get_forecast(lat: float, lon: float) -> Optional[str]:
        """Get 3-day weather forecast."""
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': WeatherConfig.API_KEY,
                'units': 'metric',
                'exclude': 'minutely,hourly,alerts,current'
            }
            response = requests.get(WeatherConfig.ONECALL_URL, params=params)
            response.raise_for_status()
            
            data = response.json()
            forecast_text = "\n\n3-Day Forecast:\n"
            
            for i in range(1, 4):
                day = data['daily'][i]
                date = datetime.fromtimestamp(day['dt']).strftime('%A')
                desc = day['weather'][0]['description'].title()
                temp = day['temp']['day']
                forecast_text += f"{date}: {temp:.1f}°C, {desc}\n"
            
            return forecast_text
        except Exception:
            return "\nCould not retrieve forecast."
    
    @staticmethod
    def get_weather_icon(icon_code: str) -> Optional[ImageTk.PhotoImage]:
        """Download and return weather icon."""
        try:
            icon_url = WeatherConfig.ICON_URL.format(icon_code=icon_code)
            response = requests.get(icon_url)
            response.raise_for_status()
            
            icon_image = Image.open(io.BytesIO(response.content))
            return ImageTk.PhotoImage(icon_image)
        except Exception:
            return None


class LocationDetector:
    """Handles location detection functionality."""
    
    @staticmethod
    def detect_current_location() -> Optional[str]:
        """Detect user's current city using IP geolocation."""
        try:
            g = geocoder.ip('me')
            return g.city
        except Exception:
            return None


class WeatherApp:
    """Main weather application class."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.theme_manager = ThemeManager()
        self.buttons = []
        
        self._setup_window()
        self._setup_ui()
        self._apply_theme()
    
    def _setup_window(self):
        """Configure the main window."""
        self.root.title("Weather App")
        self.root.geometry("400x550")
        self.root.resizable(False, False)
    
    def _setup_ui(self):
        """Create and configure UI elements."""
        # Title
        self.title_label = tk.Label(
            self.root, 
            text="Weather Forecast", 
            font=("Helvetica", 18, "bold")
        )
        self.title_label.pack(pady=20)
        
        # City input
        self.city_entry = tk.Entry(
            self.root, 
            font=("Helvetica", 14), 
            width=25, 
            justify="center"
        )
        self.city_entry.pack(pady=10)
        self.city_entry.bind('<Return>', lambda event: self.get_weather())
        
        # Buttons
        self._create_buttons()
        
        # Weather icon
        self.icon_label = tk.Label(self.root)
        self.icon_label.pack(pady=10)
        
        # Weather information
        self.result_label = tk.Label(
            self.root, 
            text="", 
            font=("Helvetica", 12), 
            justify="left", 
            wraplength=350
        )
        self.result_label.pack(pady=10)
    
    def _create_buttons(self):
        """Create application buttons."""
        button_configs = [
            ("Check Weather", self.get_weather, 12),
            ("Detect My Location", self.detect_location, 11),
            ("Toggle Theme", self.toggle_theme, 11)
        ]
        
        for text, command, font_size in button_configs:
            button = tk.Button(
                self.root, 
                text=text, 
                font=("Helvetica", font_size), 
                command=command
            )
            button.pack(pady=5)
            self.buttons.append(button)
    
    def _apply_theme(self):
        """Apply the current theme to all UI elements."""
        theme = self.theme_manager.get_current_theme()
        
        # Configure main window and labels
        self.root.configure(bg=theme["bg"])
        self.title_label.configure(bg=theme["bg"], fg=theme["fg"])
        self.result_label.configure(bg=theme["bg"], fg=theme["fg"])
        self.icon_label.configure(bg=theme["bg"])
        
        # Configure entry
        self.city_entry.configure(
            bg=theme["entry_bg"], 
            fg=theme["fg"], 
            insertbackground=theme["fg"]
        )
        
        # Configure buttons
        for button in self.buttons:
            button.configure(
                bg=theme["button_bg"], 
                fg=theme["fg"], 
                activebackground=theme["entry_bg"]
            )
    
    def detect_location(self):
        """Detect and set user's current location."""
        city = LocationDetector.detect_current_location()
        
        if city:
            self.city_entry.delete(0, tk.END)
            self.city_entry.insert(0, city)
            self.get_weather()
        else:
            messagebox.showwarning(
                "Location Error", 
                "Could not detect your location."
            )
    
    def toggle_theme(self):
        """Toggle between light and dark themes."""
        self.theme_manager.toggle_theme()
        self._apply_theme()
    
    def get_weather(self):
        """Fetch and display weather information."""
        city = self.city_entry.get().strip()
        
        if not city:
            messagebox.showwarning(
                "Input Required", 
                "Please enter a city name."
            )
            return
        
        # Get current weather
        weather_data = WeatherAPI.get_current_weather(city)
        
        if not weather_data:
            self._show_error("City not found. Please try again.")
            return
        
        # Extract weather information
        try:
            weather_info = self._format_weather_data(weather_data, city)
            self.result_label.config(text=weather_info)
            
            # Display weather icon
            icon_code = weather_data["weather"][0]["icon"]
            self._display_weather_icon(icon_code)
            
            # Add forecast if possible
            self._add_forecast(city, weather_info)
            
        except KeyError as e:
            messagebox.showerror(
                "Error", 
                f"Unexpected data format: {e}"
            )
    
    def _format_weather_data(self, data: Dict[str, Any], city: str) -> str:
        """Format weather data for display."""
        weather = data["weather"][0]
        main = data["main"]
        wind = data["wind"]
        
        return (
            f"City: {city.title()}\n"
            f"Temperature: {main['temp']:.1f}°C\n"
            f"Weather: {weather['description'].title()}\n"
            f"Humidity: {main['humidity']}%\n"
            f"Pressure: {main['pressure']} hPa\n"
            f"Wind Speed: {wind['speed']} m/s"
        )
    
    def _display_weather_icon(self, icon_code: str):
        """Display weather icon."""
        icon_photo = WeatherAPI.get_weather_icon(icon_code)
        
        if icon_photo:
            self.icon_label.config(image=icon_photo)
            self.icon_label.image = icon_photo  # Keep reference
        else:
            self.icon_label.config(image='')
    
    def _add_forecast(self, city: str, current_weather: str):
        """Add forecast information to the display."""
        lat, lon = WeatherAPI.get_coordinates(city)
        
        if lat and lon:
            forecast = WeatherAPI.get_forecast(lat, lon)
            if forecast:
                self.result_label.config(text=current_weather + forecast)
    
    def _show_error(self, message: str):
        """Display error message and clear icon."""
        self.result_label.config(text=message)
        self.icon_label.config(image='')


def main():
    """Main application entry point."""
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()