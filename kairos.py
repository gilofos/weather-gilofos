import requests
import json
from datetime import datetime, timedelta, timezone

# Συντεταγμένες για Γήλοφο
LAT, LON = 40.06, 21.80

# URL για λήψη δεδομένων - Με βροχή
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m,wind_direction_10m,rain&timezone=auto"

def get_weather():
    try:
        response = requests.get(URL, timeout=15)
        if response.status_code == 200:
            data = response.json()["current"]
            
            # Ώρα Ελλάδος (UTC+2)
            now_gr = datetime.now(timezone.utc) + timedelta(hours=2)
            current_time = now_gr.strftime("%H:%M:%S")
            
            pressure = round(data["pressure_msl"], 1)
            rain = data.get("rain", 0.0)

            # Λογική Πρόγνωσης
            if pressure >= 1022:
                status = "ΑΙΘΡΙΟΣ"
            elif 1008 <= pressure < 1022:
                status = "ΣΥΝΝΕΦΙΑ ΜΕ ΗΛΙΟ"
            else:
                status = "ΕΠΙΔΕΙΝΩΣΗ ΚΑΙΡΟΥ"

            # Λογική Τάσης Πίεσης
            try:
                with open("data.json", "r", encoding="utf-8") as f:
                    old_data = json.load(f)
                    old_p_str = str(old_data.get("pressure", pressure)).split()[0]
                    old_p_val = float(old_p_str)
            except:
                old_p_val = pressure

            trend = "↑" if pressure > old_p_val else "↓" if pressure < old_p_val else "→"

            # Σύνθεση δεδομένων - ΕΔΩ ΚΑΘΑΡΙΣΑΜΕ ΤΟΝ ΑΝΕΜΟ
            weather_data = {
                "temperature": round(data["temperature_2m"], 1),
                "humidity": data["relative_humidity_2m"],
                "pressure": f"{pressure} hPa {trend}", 
                "status": status,
                # Μόνο ταχύτητα και βροχή, χωρίς τη λέξη "Διεύθυνση"
                "wind_speed": f"{round(data['wind_speed_10m'], 1)}km/h - Βροχή:{rain}mm",
                "last_update": current_time
            }
            
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(weather_data, f, ensure_ascii=False, indent=4)
            
            print(f"Update Success: {pressure} hPa {status}")
        else:
            print(f"API Error: {response.status_code}")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    get_weather()
