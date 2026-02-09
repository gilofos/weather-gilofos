import requests
import json
from datetime import datetime, timedelta, timezone

# Συντεταγμένες για Γήλοφο
LAT, LON = 40.06, 21.80

# Ενημερωμένο URL για να παίρνουμε και την κατεύθυνση του ανέμου (wind_direction_10m)
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m,wind_direction_10m&timezone=auto"

def get_weather():
    try:
        response = requests.get(URL, timeout=15)
        if response.status_code == 200:
            data = response.json()["current"]
            
            # Ώρα Ελλάδος (UTC+2) - Το GitHub Actions τρέχει σε UTC
            now_gr = datetime.now(timezone.utc) + timedelta(hours=2)
            current_time = now_gr.strftime("%H:%M:%S")
            
            pressure = round(data["pressure_msl"], 1)

            # Λογική ειδοποίησης - Παραμένει το 1007 ως όριο
            if pressure < 1007:
                status = "ΕΠΙΔΕΙΝΩΣΗ ΚΑΙΡΟΥ"
            else:
                status = "ΚΑΙΡΟΣ ΣΤΑΘΕΡΟΣ"

            # --- Λογική για το Βελάκι Πίεσης ---
            try:
                with open("data.json", "r", encoding="utf-8") as f:
                    old_data = json.load(f)
                    # Αφαιρούμε το βελάκι αν υπάρχει για να συγκρίνουμε μόνο αριθμούς
                    old_p_val = float(str(old_data.get("pressure", pressure)).split()[0])
            except:
                old_p_val = pressure

            if pressure > old_p_val:
                trend = "↑"
            elif pressure < old_p_val:
                trend = "↓"
            else:
                trend = "→"

            # --- Μετατροπή Μοιρών Ανέμου σε Γράμματα ---
            deg = data["wind_direction_10m"]
            directions = ["Β", "ΒΑ", "Α", "ΝΑ", "Ν", "ΝΔ", "Δ", "ΒΔ"]
            ix = int((deg + 22.5) / 45) % 8
            wind_dir_cardinal = directions[ix]

            # Δημιουργία των δεδομένων για την HTML
            weather_data = {
                "temperature": round(data["temperature_2m"], 1),
                "humidity": data["relative_humidity_2m"],
                "pressure": f"{pressure} {trend}", # Προσθήκη trend
                "status": status,
                "wind_speed": round(data["wind_speed_10m"], 1),
                "wind_dir": wind_dir_cardinal, # Προσθήκη κατεύθυνσης
                "last_update": current_time
            }
            
            # Αποθήκευση στο data.json
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(weather_data, f, ensure_ascii=False, indent=4)
            
            print(f"Ενημέρωση GitHub OK: {current_time} | Πίεση: {pressure}{trend} | Άνεμος: {wind_dir_cardinal}")
        else:
            print(f"Σφάλμα API: {response.status_code}")
    except Exception as e:
        print(f"Σφάλμα κατά την εκτέλεση: {e}")

if __name__ == "__main__":
    get_weather()
