import requests
import json
from datetime import datetime, timedelta, timezone

# Συντεταγμένες για Γήλοφο
LAT, LON = 40.06, 21.80

def get_weather():
    try:
        # Λήψη δεδομένων από το Open-Meteo
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m,wind_direction_10m,rain&timezone=auto"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()["current"]
            
            # Ώρα Ελλάδος
            now_gr = datetime.now(timezone.utc) + timedelta(hours=2)
            current_time = now_gr.strftime("%H:%M:%S")
            
            temp = round(data["temperature_2m"], 1)
            hum = data["relative_humidity_2m"]
            pres = round(data["pressure_msl"], 1)
            wind_sp = round(data["wind_speed_10m"], 1)
            rain = data.get("rain", 0.0)
            
            # Υπολογισμός κατεύθυνσης ανέμου
            degrees = data["wind_direction_10m"]
            directions = ["Β", "ΒΑ", "Α", "ΝΑ", "Ν", "ΝΔ", "Δ", "ΒΔ"]
            idx = int((degrees + 22.5) / 45) % 8
            wind_dir = directions[idx]

            # Πρόγνωση βάσει πίεσης
            if pres >= 1022: status = "ΑΙΘΡΙΟΣ"
            elif 1008 <= pres < 1022: status = "ΣΥΝΝΕΦΙΑ"
            else: status = "ΕΠΙΔΕΙΝΩΣΗ"

            # Δημιουργία του αρχείου data.json
            weather_data = {
                "temperature": temp,
                "humidity": hum,
                "pressure": f"{pres} hPa",
                "status": status,
                "wind_speed": f"{wind_sp} km/h {wind_dir} - Βροχή: {rain}mm",
                "last_update": current_time
            }
            
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(weather_data, f, ensure_ascii=False, indent=4)
            
            print(f"Επιτυχία! Θερμοκρασία: {temp}°C")
        else:
            print("Σφάλμα API")
    except Exception as e:
        print(f"Σφάλμα: {e}")

if __name__ == "__main__":
    get_weather()
