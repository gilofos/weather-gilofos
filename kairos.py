import requests
import json
from datetime import datetime, timedelta, timezone

# Συντεταγμένες για Γήλοφο Γρεβενών
LAT = 40.06
LON = 21.80

# URL για Open-Meteo (Τρέχοντα + Ωριαία + Ημερήσια Πρόγνωση)
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m&hourly=temperature_2m&daily=weathercode,temperature_2m_max,temperature_2m_min&timezone=auto"

def get_weather():
    try:
        response = requests.get(URL)
        data = response.json()

        if response.status_code == 200:
            current = data["current"]
            hourly = data["hourly"]
            daily = data["daily"]
            
            # Ώρα Ελλάδας
            current_time = (datetime.now(timezone.utc) + timedelta(hours=2)).strftime("%H:%M:%S")

            # Πίεση στα 1050μ
            station_pressure = current["surface_pressure"]
            sea_level_pressure = round(station_pressure + 124.5)

            # Alert Logic
            alert_status = False
            if sea_level_pressure < 1000 or current["wind_speed_10m"] > 50:
                alert_status = True

            # Δεδομένα για το γράφημα (τελευταίες 24 ώρες)
            history_temp = hourly["temperature_2m"][:24]
            history_labels = [t.split('T')[1] for t in hourly["time"][:24]]

            # Δεδομένα για πρόβλεψη εβδομάδας
            forecast_days = []
            days_names = ["Κυρ", "Δευ", "Τρι", "Τετ", "Πεμ", "Παρ", "Σαβ"]
            
            for i in range(7):
                date_obj = datetime.strptime(daily["time"][i], "%Y-%m-%d")
                forecast_days.append({
                    "day": days_names[date_obj.weekday()],
                    "temp_max": round(daily["temperature_2m_max"][i]),
                    "temp_min": round(daily["temperature_2m_min"][i]),
                    "code": daily["weathercode"][i]
                })

            weather_data = {
                "temperature": round(current["temperature_2m"], 1),
                "humidity": current["relative_humidity_2m"],
                "pressure": sea_level_pressure,
                "wind_speed": round(current["wind_speed_10m"], 1),
                "last_update": current_time,
                "alert": alert_status,
                "status": "ΕΠΙΔΕΙΝΩΣΗ" if alert_status else "ΟΜΑΛΟΣ ΚΑΙΡΟΣ",
                "chart_data": history_temp,
                "chart_labels": history_labels,
                "forecast": forecast_days
            }

            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(weather_data, f, ensure_ascii=False, indent=4)
            
            print(f"Ενημέρωση {current_time}: OK")

    except Exception as e:
        print(f"Σφάλμα: {e}")

if __name__ == "__main__":
    get_weather()
