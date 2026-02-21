import requests
import json
from datetime import datetime

# Στοιχεία για Γήλοφο
LAT = 40.06
LON = 21.80
STATION_NAME = "ΓΗΛΟΦΟΣ"

def get_weather():
    # Ζητάμε τρέχοντα και ημερήσια στοιχεία (max/min, βροχή, ριπές)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,is_day,precipitation,surface_pressure,wind_speed_10m,wind_direction_10m,cloud_cover&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,wind_gusts_10m_max&timezone=auto"
    
    try:
        response = requests.get(url)
        res_data = response.json()
        current = res_data['current']
        daily = res_data['daily']
        
        # Βασικές μετρήσεις
        temp = current['temperature_2m']
        hum = current['relative_humidity_2m']
        pres = current['surface_pressure']
        wind_s = current['wind_speed_10m']
        wind_d = current['wind_direction_10m']
        clouds = current['cloud_cover']
        is_day = current['is_day']
        
        # Ημερήσια στοιχεία
        t_max = daily['temperature_2m_max'][0]
        t_min = daily['temperature_2m_min'][0]
        rain_sum = daily['precipitation_sum'][0]
        gust = daily['wind_gusts_10m_max'][0]

        time_str = datetime.utcnow().strftime("%H:%M:%S")

        # --- ΚΑΤΑΣΤΑΣΗ ΜΕ ΕΙΚΟΝΙΔΙΑ ---
        if clouds <= 25:
            weather_desc = "ΛΙΑΚΑΔΑ.ΑΙΘΡΙΟΣ ☀️" if is_day else "ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ 🌙"
        elif 25 < clouds <= 60:
            weather_desc = "ΑΡΑΙΗ ΣΥΝΝΕΦΙΑ 🌤️"
        else:
            weather_desc = "ΣΥΝΝΕΦΙΑ ☁️"

        # --- ΔΙΑΜΟΡΦΩΣΗ ΑΝΕΜΟΥ: Α, [ταχύτητα] ΝΔΜΒ Α ---
        wind_label = f"Α, {wind_s} ΝΔΜΒ Α"

        # ΤΟ ΠΛΗΡΕΣ ΠΑΚΕΤΟ ΓΙΑ ΤΟ SITE
        weather_data = {
            "temperature": temp,
            "temp_max": t_max,
            "temp_min": t_min,
            "humidity": hum,
            "pressure": pres,
            "wind_speed": wind_s,
            "wind_gust": gust,
            "wind_dir": wind_d,
            "wind_text": wind_label,
            "rain": rain_sum,
            "status": weather_desc,
            "last_update": time_str,
            "time": time_str
        }

        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(weather_data, f, ensure_ascii=False, indent=4)

        # Απλή σελίδα index.html
        html_content = f"<html><body style='background:#121212;color:white;text-align:center;'><h1>{STATION_NAME}</h1><h2>{weather_desc}</h2><p>{temp}°C - {hum}%</p><p>{wind_label}</p></body></html>"
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
            
    except Exception as e:
        print(f"Σφάλμα: {e}")

if __name__ == "__main__":
    get_weather(
