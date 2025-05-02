🌦️ Weather Forecast App (Python + Tkinter)
A professional-grade desktop weather application built with Python and Tkinter. It features real-time weather conditions, a 3-day forecast, light/dark theme switching, and automatic location detection via IP.

🚀 Features
✅ Real-time current weather by city name

🌤️ 3-day daily forecast (using OpenWeatherMap One Call API)

🗺️ Auto location detection with IP geolocation (using geocoder)

🌓 Light/Dark theme toggle

🌡️ Styled GUI using tkinter and Pillow for weather icons

💬 Clean and extendable object-oriented design

📸 Screenshot
(Add a screenshot of the running app here if you'd like)

🧱 Requirements
Python 3.7+

Required libraries:

bash
Copy
Edit
pip install requests Pillow geocoder
🔧 Setup Instructions
Clone the repository (or copy the code):

bash
Copy
Edit
git clone https://github.com/bednahkitonyi/WeatherApp.git
cd weather-app
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Set your OpenWeatherMap API Key:

Open the weather_app.py file and replace:

python
Copy
Edit
API_KEY = "your_api_key_here"
with your actual OpenWeatherMap API key.

Run the application:

bash
Copy
Edit
python weather_app.py
📦 Packaging to EXE (Optional)
To build a desktop .exe:

bash
Copy
Edit
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed weather_app.py
The executable will appear in the /dist folder.

📁 File Structure
Copy
Edit
weather-app/
├── weather_app.py
├── README.md
└── requirements.txt
(You can generate requirements.txt with pip freeze > requirements.txt)

💡 To Do (Ideas for Future)
Add hourly forecast support

Add weather map view (using folium or basemap)

Add UV index, sunrise/sunset, wind direction

Support multiple languages

🧑‍💻 Author
Created by [Bednah Kitonyi]
Feel free to fork, modify
