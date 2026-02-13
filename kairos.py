import requests
import json
from datetime import datetime

# Συντεταγμένες για Γήλοφο (Υψόμετρο ~1050μ)
LAT = 39.88
LON = 21.80

def get_weather():
    try:
        # Παίρνουμε τα δεδομένα από το Open-Meteo
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,surface_pressure,precipitation,wind_speed_10m,wind_direction_10m&timezone=auto"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()['current']
        
        temp = data['temperature_2m']
        precip = data['precipitation']
        
        # ΛΟΓΙΚΗ ΓΙΑ ΧΙΟΝΙ/ΒΡΟΧΗ
        if temp <= 1.5 and precip > 0:
            weather_type = "ΧΙΟΝΟΠΤΩΣΗ ❄️"
        elif temp <= 3.0 and precip > 0:
            weather_type = "ΧΙΟΝΟΝΕΡΟ 🌨️"
        elif precip > 0:
            weather_type = "ΒΡΟΧΗ 💧"
        else:
            weather_type = "ΣΥΝΝΕΦΙΑ ☁️" if temp < 10 else "ΚΑΘΑΡΟΣ ☀️"

        # Προετοιμασία των δεδομένων για το site
        weather_data = {
            "temperature": temp,
            "pressure": data['surface_pressure'],
            "wind_speed": data['wind_speed_10m'],
            "wind_dir": data['wind_direction_10m'],
            "rain": precip,
            "weather_label": weather_type,
            "time": datetime.now().strftime("%H:%M:%S")
        }
        
        # Αποθήκευση στο data.json για να το διαβάσει το site
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(weather_data, f, ensure_ascii=False, indent=4)
            
        print(f"Ενημερώθηκε: {weather_type} με {temp}°C")

    except Exception as e:
        print(f"Σφάλμα: {e}")

if __name__ == "__main__":
    get_weather()
