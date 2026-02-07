import requests
import json
from datetime import datetime, timedelta, timezone

# Ρυθμίσεις
API_KEY = "3bc8527a20c786500ccba4652c42c262"
CITY = "Ghilofos,GR"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=el"

def get_weather():
    try:
        response = requests.get(URL)
        data = response.json()

        if response.status_code == 200:
            # Ρύθμιση ώρας Ελλάδας (UTC+2) - Χωρίς έξτρα βιβλιοθήκες
            offset = timezone(timedelta(hours=2))
            current_time = datetime.now(offset).strftime("%H:%M:%S")

            # Διόρθωση πίεσης για το υψόμετρο του Γηλόφου (1050μ)
            # Προσθέτουμε 118 hPa για αναγωγή στη στάθμη της θάλασσας
            sea_level_pressure = data["main"]["pressure"] + 118

            weather_info = {
                "temperature": round(data["main"]["temp"], 1),
                "humidity": data["main"]["humidity"],
                "pressure": sea_level_pressure,
                "description": data["weather"][0]["description"].capitalize(),
                "icon": data["weather"][0]["icon"],
                "last_update": current_time
            }

            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(weather_info, f, ensure_ascii=False, indent=4)
            
            print(f"Επιτυχής ενημέρωση: {current_time}")
        else:
            print(f"Σφάλμα API: {data.get('message')}")

    except Exception as e:
        print(f"Σφάλμα συστήματος: {e}")

if __name__ == "__main__":
    get_weather()
