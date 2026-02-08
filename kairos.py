import requests
import json
import math
from datetime import datetime, timedelta, timezone

# --- ΡΥΘΜΙΣΕΙΣ ΓΗΛΟΦΟΥ ---
LAT = 40.06
LON = 21.80
ELEVATION = 1050  # Το ακριβές υψόμετρο σε μέτρα

# URL Open-Meteo
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,weathercode&timezone=auto"

def get_sea_level_pressure(p_station, temp_c, elevation):
    """
    Υπολογισμός πίεσης στη στάθμη της θάλασσας (QNH) 
    χρησιμοποιώντας τον βαρομετρικό τύπο.
    """
    temp_k = temp_c + 273.15 # Μετατροπή σε Kelvin
    # Διεθνής τύπος για τη μείωση της πίεσης στη στάθμη της θάλασσας
    p_sealevel = p_station * (1 - ((0.0065 * elevation) / (temp_k + (0.0065 * elevation)))) ** -5.257
    return round(p_sealevel, 1)

def get_weather():
    try:
        response = requests.get(URL, timeout=15)
        if response.status_code == 200:
            data = response.json()
            current = data["current"]
            
            temp = current["temperature_2m"]
            p_surf = current["surface_pressure"] # Πίεση στο υψόμετρο του σταθμού
            
            # Επιστημονικός υπολογισμός αντί για σταθερή πρόσθεση
            msl_pressure = get_sea_level_pressure(p_surf, temp, ELEVATION)
            
            now = datetime.now(timezone.utc) + timedelta(hours=2)
            current_time = now.strftime("%H:%M:%S")

            # Λογική Alert (Επιδείνωση αν η πίεση πέσει απότομα ή είναι χαμηλή)
            is_alert = False
            if msl_pressure < 1005 or current["wind_speed_10m"] > 35:
                is_alert = True

            weather_info = {
                "temperature": round(temp, 1),
                "humidity": current["relative_humidity_2m"],
                "pressure": int(msl_pressure), # Το μετατρέπουμε σε ακέραιο για το UI
                "wind_speed": round(current["wind_speed_10m"], 1),
                "last_update": current_time,
                "alert": is_alert
            }

            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(weather_info, f, ensure_ascii=False, indent=4)
            
            print(f"Update: {current_time} | Station: {p_surf} | MSL: {msl_pressure}")
        else:
            print("API Error")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_weather()
