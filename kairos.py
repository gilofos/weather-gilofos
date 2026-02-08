import requests
import json
from datetime import datetime, timedelta, timezone

# Συντεταγμένες για Γήλοφο Γρεβενών
LAT = 40.06
LON = 21.80

# URL για Open-Meteo
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,wind_direction_10m&timezone=auto"

def get_weather():
    try:
        response = requests.get(URL)
        data = response.json()

        if response.status_code == 200:
            current = data["current"]
            
            # Ώρα Ελλάδας για το GitHub Actions
            current_time = (datetime.now(timezone.utc) + timedelta(hours=2)).strftime("%H:%M:%S")

            # Υπολογισμός πίεσης στη θάλασσα (MSL) - Γήλοφος ~1050μ
            sea_level_pressure = round(current["surface_pressure"] + 119)
