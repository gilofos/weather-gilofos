import requests
import json
from datetime import datetime

# --- ΡΥΘΜΙΣΕΙΣ ---
LAT = 40.06
LON = 21.80
# Χρησιμοποιούμε pressure_msl για πίεση στη στάθμη της θάλασσας
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,apparent_temperature,relative_humidity_2m,pressure_msl,wind_speed_10m,wind_direction_10m,weather_code&hourly=temperature_2m,weather_code&timezone=auto&forecast_days=1"

def get_weather_icon(code):
    """Αντιστοίχιση κωδικών Open-Meteo σε Emojis"""
    mapping = {
        0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️", 
        45: "🌫️", 48: "🌫️", 
        51: "🌦️", 53: "🌦️", 55: "🌦️",
        61: "🌧️", 63: "🌧️", 65: "🌧️",
        71: "❄️", 73: "❄️", 75: "❄️",
        95: "⛈️"
    }
    return mapping.get(code, "🌡️")

def get_weather():
    try:
        response = requests.get(URL)
        data = response.json()

        if response.status_code == 200:
            current = data["current"]
            hourly = data["hourly"]
            
            # Ώρα ενημέρωσης (Τοπική ώρα συστήματος)
            current_time = datetime.now().strftime("%H:%M:%S")

            # --- ΥΠΟΛΟΓΙΣΜΟΣ ALERTS ---
            pressure = round(current["pressure_msl"], 1)
            wind = round(current["wind_speed_10m"], 1)
            alert_message = ""

            # Έλεγχος Πίεσης
            if pressure < 1000:
                alert_message = "⚠️ ALERT: Πολύ χαμηλή πίεση! Πιθανή κακοκαιρία."
            elif pressure < 1007:
                alert_message = "☁️ Προσοχή: Χαμηλή πίεση. Ο καιρός αλλάζει."
            elif pressure > 1025:
                alert_message = "☀️ Υψηλή πίεση. Σταθερός καιρός / Καλοκαιρία."

            # Έλεγχος Ανέμου (π.χ. πάνω από 40 km/h)
            if wind > 40:
                alert_message += " 🚩 Προσοχή: Πολύ δυνατός άνεμος!"

            # --- ΠΡΟΓΝΩΣΗ 24 ΩΡΩΝ (Ανά 3 ώρες) ---
            forecast_list = []
            for i in range(0, 24, 3):
                forecast_list.append({
                    "time": hourly["time"][i][-5:], 
                    "temp": round(hourly["temperature_2m"][i], 1),
                    "icon": get_weather_icon(hourly["weather_code"][i])
                })

            # --- ΔΟΜΗ JSON ---
            weather_info = {
                "location": "Γήλοφος Γρεβενών",
                "temperature": round(current["temperature_2m"], 1),
                "feels_like": round(current["apparent_temperature"], 1),
                "icon": get_weather_icon(current["weather_code"]),
                "humidity": current["relative_humidity_2m"],
                "pressure": pressure,
                "wind_speed": wind,
                "wind_dir": current["wind_direction_10m"],
                "alert": alert_message,
                "description": "Live Weather Data",
                "last_update": current_time,
                "forecast": forecast_list
            }

            # Αποθήκευση στο αρχείο data.json
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(weather_info, f, ensure_ascii=False, indent=4)
            
            print(f"Επιτυχής ενημέρωση: {current_time} | Πίεση: {pressure} hPa")

        else:
            print(f"API Error: {response.status_code}")

    except Exception as e:
        print(f"Σφάλμα: {e}")

if __name__ == "__main__":
    get_weather()
