import requests
import json
from datetime import datetime, timedelta, timezone

# Συντεταγμένες για Γήλοφο
LAT, LON = 40.06, 21.80

# URL για λήψη δεδομένων και κατεύθυνσης ανέμου
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m,wind_direction_10m&timezone=auto"

def get_weather():
    try:
        response = requests.get(URL, timeout=15)
        if response.status_code == 200:
            data = response.json()["current"]
            
            # Ώρα Ελλάδος
            now_gr = datetime.now(timezone.utc) + timedelta(hours=2)
            current_time = now_gr.strftime("%H:%M:%S")
            
            pressure = round(data["pressure_msl"], 1)

            # Λογική ειδοποίησης (Όριο 1007)
            if pressure < 1007:
                status = "ΕΠΙΔΕΙΝΩΣΗ ΚΑΙΡΟΥ"
            else:
                status = "ΚΑΙΡΟΣ ΣΤΑΘΕΡΟΣ"

            # --- Λογική για το Βελάκι Πίεσης (Τάση) ---
            try:
                with open("data.json", "r", encoding="utf-8") as f:
                    old_data = json.load(f)
                    # Παίρνουμε μόνο τον αριθμό για τη σύγκριση
                    old_p_str = str(old_data.get("pressure", pressure)).split()[0]
                    old_p_val = float(old_p_str)
            except:
                old_p_val = pressure

            if pressure > old_p_val:
                trend = "↑"
            elif pressure < old_p_val:
                trend = "↓"
            else:
                trend = "→"

            # --- Μετατροπή Μοιρών σε Ελληνικά Γράμματα ---
            deg = data["wind_direction_10m"]
            directions = ["Β", "ΒΑ", "Α", "ΝΑ", "Ν", "ΝΔ", "Δ", "ΒΔ"]
            ix = int((deg + 22.5) / 45) % 8
            wind_dir_cardinal = directions[ix]

            # Δημιουργία των δεδομένων - Αφαίρεσα το hPa από εδώ για να μη βγαίνει διπλό
            weather_data = {
                "temperature": round(data["temperature_2m"], 1),
                "humidity": data["relative_humidity_2m"],
                "pressure": f"{pressure} {trend}", 
                "status": status,
                "wind_speed": f"{round(data['wind_speed_10m'], 1)} km/h {wind_dir_card
