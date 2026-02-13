import requests
import json
from datetime import datetime

# Συντεταγμένες για Γήλοφο
LAT = 39.88
LON = 21.80

def get_weather():
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,surface_pressure,precipitation,wind_speed_10m,wind_direction_10m&timezone=auto"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()['current']
        
        temp = data['temperature_2m']
        precip = data['precipitation']
        hum = data['relative_humidity_2m']
        pres = data['surface_pressure']
        time_now = datetime.now().strftime("%H:%M:%S")
        
        # ΕΛΕΓΧΟΣ ΜΕΡΑΣ/ΝΥΧΤΑΣ
        ora = datetime.now().hour
        is_night = ora >= 18 or ora <= 7
        
        # ΛΟΓΙΚΗ ΠΡΟΓΝΩΣΗΣ
        if temp <= 1.5 and precip > 0:
            weather_type = "ΧΙΟΝΟΠΤΩΣΗ ❄️"
        elif temp <= 3.0 and precip > 0:
            weather_type = "ΧΙΟΝΟΝΕΡΟ 🌨️"
        elif precip > 0:
            weather_type = "ΒΡΟΧΗ 💧"
        else:
            if pres >= 915:
                weather_type = "ΑΣΤΕΡΟΣ 🌙" if is_night else "ΑΙΘΡΙΟΣ ☀️"
            elif pres >= 905:
                weather_type = "ΞΑΣΤΕΡΙΑ 🌌" if is_night else "ΣΥΝΝΕΦΙΑ ΜΕ ΗΛΙΟ ⛅"
            else:
                weather_type = "ΣΥΝΝΕΦΙΑ ☁️"

        # ΤΟ "ΚΛΕΙΔΙ": Προσθέτουμε το 'status' για να το βλέπει η γραμμή 178 του HTML
        weather_data = {
            "temperature": temp,
            "humidity": hum,
            "pressure": pres,
            "wind_speed": data['wind_speed_10m'],
            "wind_dir": data['wind_direction_10m'],
            "rain": precip,
            "status": weather_type,        # ΑΥΤΟ ΕΙΝΑΙ ΠΟΥ ΛΕΙΠΕΙ!
            "weather_label": weather_type,
            "condition": weather_type,
            "time": time_now,
            "last_update": time_now,
            "updated_at": time_now
        }
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(weather_data, f, ensure_ascii=False, indent=4)
            
        print(f"Ενημερώθηκε: {weather_type}")

    except Exception as e:
        print(f"Σφάλμα: {e}")

if __name__ == "__main__":
    get_weather()
