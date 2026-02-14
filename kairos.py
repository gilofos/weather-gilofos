import requests
import json
from datetime import datetime

# Συντεταγμένες για Γήλοφο
LAT = 39.88
LON = 21.80

def get_direction(degrees):
    """Μετατρέπει τις μοίρες στα 8 βασικά σημεία"""
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
        pres_station = data['surface_pressure']
        
        # --- ΔΙΟΡΘΩΣΗ ΠΙΕΣΗΣ ΓΙΑ 1050μ ΥΨΟΜΕΤΡΟ ---
        pres_sea = pres_station + 103 
        
        wind_spd = data['wind_speed_10m']
        wind_deg = data['wind_direction_10m']
        time_now = datetime.now().strftime("%H:%M:%S")
        
        # Ονομασία ανέμου (Β, ΝΑ, κτλ)
        wind_cardinal = get_direction(wind_deg)
        
        # 2. Έλεγχος Μέρας/Νύχτας (Νύχτα: 18:00 έως 07:00)
        ora = datetime.now().hour
        is_night = ora >= 18 or ora <= 7
        
        # 3. Λογική Πρόγνωσης (Σφραγισμένη!)
        if precip > 0:
            if temp <= 1.5:
                weather_type = "ΧΙΟΝΟΠΤΩΣΗ ❄️"
            elif temp <= 3.0:
                weather_type = "ΧΙΟΝΟΝΕΡΟ 🌨️"
            else:
                weather_type = "ΒΡΟΧΗ 💧"
        else:
            # Όταν ΔΕΝ βρέχει, κοιτάμε την πίεση και την ώρα
            if pres_sea >= 1016:
                if is_night:
                    weather_type = "ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ 🌌"
                else:
                    weather_type = "ΗΛΙΟΦΑΝΕΙΑ ☀️" if pres_sea >= 1022 else "ΔΙΑΣΤΗΜΑΤΑ ΗΛΙΟΦΑΝΕΙΑΣ ⛅"
            elif pres_sea >= 1008:
                weather_type = "ΣΥΝΝΕΦΙΑ ☁️"
            else:
                weather_type = "ΒΑΡΙΑ ΣΥΝΝΕΦΙΑ ☁️☁️"

        # 4. Αποστολή στο data.json
        weather_data = {
            "temperature": temp,
            "humidity": hum,
            "pressure": round(pres_sea, 1),
            "wind_speed": wind_spd,
            "wind_dir": wind_deg,
            "wind_text": wind_cardinal,
            "rain": precip,
            "status": weather_type,
            "time": time_now,
            "last_update": time_now
        }
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(weather_data, f, ensure_ascii=False, indent=4)
            
        print(f"[{time_now}] Ενημερώθηκε! Πρόγνωση: {weather_type}")

    except Exception as e:
        print(f"Σφάλμα: {e}")

if __name__ == "__main__":
    get_weather()
