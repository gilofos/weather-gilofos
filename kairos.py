import requests
import json
from datetime import datetime, timedelta, timezone

# Συντεταγμένες για Γήλοφο
LAT, LON = 40.06, 21.80

# URL για λήψη δεδομένων (θερμοκρασία, υγρασία, πίεση, ταχύτητα & κατεύθυνση ανέμου)
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m,wind_direction_10m&timezone=auto"

def get_weather():
    try:
        response = requests.get(URL, timeout=15)
        if response.status_code == 200:
            data = response.json()["current"]
            
            # Ώρα Ελλάδος (UTC+2 ή +3 ανάλογα την εποχή)
            now_gr = datetime.now(timezone.utc) + timedelta(hours=2)
            current_time = now_gr.strftime("%H:%M:%S")
            
            pressure = round(data["pressure_msl"], 1)

            # Λογική ειδοποίησης - Το όριο σου παραμένει στο 1007
            if pressure < 1007:
                status = "ΕΠΙΔΕΙΝΩΣΗ ΚΑΙΡΟΥ"
            else:
                status = "ΚΑΙΡΟΣ ΣΤΑΘΕΡΟΣ"

            # --- Λογική για το Βελάκι Πίεσης (Τάση) ---
            try:
                with open("data.json", "r", encoding="utf-8") as f:
                    old_data = json.load(f)
                    # Παίρνουμε τον αριθμό από την παλιά εγγραφή π.χ. "1006.3 hPa ↓"
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

            # --- Μετατροπή Μοιρών Ανέμου σε Ελληνικές Κατευθύνσεις ---
            deg = data["wind_direction_10m"]
            directions = ["Β", "ΒΑ", "Α", "ΝΑ", "Ν", "ΝΔ", "Δ", "ΒΔ"]
            ix = int((deg + 22.5) / 45) % 8
            wind_dir_cardinal = directions[ix]

            # Δημιουργία των δεδομένων για το data.json
            weather_data = {
                "temperature": round(data["temperature_2m"], 1),
                "humidity": data["relative_humidity_2m"],
                "pressure": f"{pressure} hPa {trend}", # Το βελάκι μπήκε μετά το hPa
                "status": status,
                "wind_speed": f"{round(data['wind_speed_10m'], 1)} km/h {wind_dir_cardinal}", # Ταχύτητα και Κατεύθυνση μαζί
                "last_update": current_time
            }
            
            # Αποθήκευση στο αρχείο
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(weather_data, f, ensure_ascii=False, indent=4)
            
            print(f"Ενημέρωση OK: {current_time} | Πίεση: {pressure} {trend} | Άνεμος: {wind_dir_cardinal}")
        else:
            print(f"Πρόβλημα με το API: {response.status_code}")
    except Exception as e:
        print(f"Σφάλμα συστήματος: {e}")

if __name__ == "__main__":
    get_weather()
