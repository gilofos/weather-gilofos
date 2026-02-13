import requests
import json
from datetime import datetime

# Συντεταγμένες για Γήλοφο
LAT = 39.88
LON = 21.80

def get_direction(degrees):
    """Μετατρέπει τις μοίρες σε ορίζοντα (Β, Ν, Α, Δ)"""
    directions = ["Β", "ΒΑ", "Α", "ΝΑ", "Ν", "ΝΔ", "Δ", "ΒΔ"]
    idx = int((degrees + 22.5) / 45) % 8
    return directions[idx]

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
        wind_spd = data['wind_speed_10m']
        wind_deg = data['wind_direction_10m']
        time_now = datetime.now().strftime("%H:%M:%S")
        
        # Μετατροπή διεύθυνσης ανέμου
        wind_cardinal = get_direction(wind_deg)
        wind_full = f"{wind_deg}° ({wind_cardinal})" # Παράδειγμα: 277° (Δ)
        
        # 2. Έλεγχος Μέρας/Νύχτας
        ora = datetime.now().hour
        is_night = ora >= 18 or ora <= 7
        
        # 3. Λογική Πρόγνωσης για τον Γήλοφο
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

        # 4. Αποστολή στο data.json
        weather_data = {
            "temperature": temp,
            "humidity": hum,
            "pressure": pres,
            "wind_speed": wind_spd,
            "wind_dir": wind_full,  # Τώρα είναι διορθωμένο
            "rain": precip,
            "status": weather_type,
            "weather_label": weather_type,
            "condition": weather_type,
            "time": time_now,
            "last_update": time_now,
            "updated_at": time_now
        }
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(weather_data, f, ensure_ascii=False, indent=4)
            
        print(f"Ενημερώθηκε: {weather_type} | Άνεμος: {wind_full}")

    except Exception as e:
        print(f"Σφάλμα: {e}")

if __name__ == "__main__":
    get_weather()
