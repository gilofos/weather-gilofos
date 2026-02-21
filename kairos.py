import requests
from datetime import datetime

# Στοιχεία για Γήλοφο
LAT = 40.0000  
LON = 21.0000
STATION_NAME = "ΓΗΛΟΦΟΣ"

def get_weather():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,is_day,precipitation,rain,showers,snowfall,weather_code,cloud_cover,surface_pressure,wind_speed_10m,wind_direction_10m&timezone=auto"
    
    try:
        response = requests.get(url)
        data = response.json()['current']
        
        temp = data['temperature_2m']
        hum = data['relative_humidity_2m']
        wind_speed = data['wind_speed_10m']
        wind_dir = data['wind_direction_10m']
        pressure = data['surface_pressure']
        clouds = data['cloud_cover']
        is_day = data['is_day']

        # ΩΡΑ UTC (Όπως ήταν χθες)
        utc_time = datetime.utcnow().strftime("%H:%M:%S")
        
        # --- ΠΡΟΣΔΙΟΡΙΣΜΟΣ ΚΑΤΕΥΘΥΝΣΗΣ ΑΝΕΜΟΥ ---
        directions = ["ΒΟΡΙΑΣ", "ΒΑ", "ΑΝΑΤΟΛΙΚΟΣ", "ΝΑ", "ΝΟΤΙΑΣ", "ΝΔ", "ΔΥΤΙΚΟΣ", "ΒΔ"]
        idx
