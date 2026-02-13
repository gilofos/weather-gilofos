import requests
import json
from datetime import datetime

# Συντεταγμένες για Γήλοφο
LAT = 39.88
LON = 21.80

def get_weather():
    try:
        # 1. Λήψη δεδομένων από το API
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,surface_pressure,precipitation,wind_speed_10m,wind_direction_10m&timezone=auto"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()['current']
        
        temp = data['temperature_2m']
        precip = data['precipitation']
        hum = data['relative_humidity_2m']
        pres = data['surface_pressure']
        time_now = datetime.now().strftime("%H:%M:%S")
        
        # 2. Η ΛΟΓΙΚΗ ΤΟΥ ΑΧΙΛΛΕΑ (Πίεση και Υετός)
        if temp <= 1.5 and precip > 0:
            weather_type = "ΧΙΟΝΟΠΤΩΣΗ ❄️"
        elif temp <= 3.0 and precip > 0:
            weather_type = "ΧΙΟΝΟΝΕΡΟ 🌨️"
        elif precip > 0:
            weather_type = "ΒΡΟΧΗ 💧"
        else:
            # Έλεγχος βάσει πίεσης για τον Γήλοφο
            if pres >= 1020:
                weather_type = "ΑΙΘΡΙΟΣ ☀️"
            elif pres >= 1007:
                weather_type = "ΣΥΝΝΕΦΙΑ ΜΕ ΗΛΙΟ ⛅"
            else:
                weather_type = "ΣΥΝΝΕΦΙΑ ☁️"

        # 3. Προετοιμασία δεδομένων για το site
        weather_data = {
            "temperature": temp,
            "humidity": hum,
            "pressure": pres,
            "wind_speed": data['wind_speed_10m'],
            "wind_dir": data['wind_direction_10m'],
            "rain": precip,
            "weather_label": weather_type,
            "condition": weather_type,
            "time": time_now,
            "last_update": time_now,
            "updated_at": time_now
        }
        
        # 4. Αποθήκευση στο data.json
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(weather_data, f, ensure_ascii=False, indent=4)
            
        print(f"Ενημερώθηκε επιτυχώς: {weather_type} ({pres} hPa)")

    except Exception as e:
        print(f"Σφάλμα κατά την ενημέρωση: {e}")

if __name__ == "__main__":
    get_weather()
