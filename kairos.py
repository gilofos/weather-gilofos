import requests
import json
from datetime import datetime, timedelta, timezone

# Συντεταγμένες για Γήλοφο Γρεβενών
LAT = 40.06
LON = 21.80
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,surface_pressure&timezone=auto"

def get_weather():
    try:
        response = requests.get(URL)
        data = response.json()

        if response.status_code == 200:
            current = data["current"]
            # Ώρα Ελλάδας
            offset = timezone(timedelta(hours=2))
            current_time = datetime.now(offset).strftime("%H:%M:%S")

            # Υπολογισμός πίεσης στη θάλασσα (προσεγγιστικά +118 hPa για το υψόμετρο του Γηλόφου)
            sea_level_pressure = round(current["surface_pressure"] + 118)

            weather_info = {
                "temperature": round(current["temperature_2m"], 1),
                "humidity": current["relative_humidity_2m"],
                "pressure": sea_level_pressure,
                "description": "Ενημερωμένο",
                "last_update": current_time
            }

            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(weather_info, f, ensure_ascii=False, indent=4)
            
            print(f"Update Done: {current_time} | Temp: {current['temperature_2m']}°C")
        else:
            print("API Error")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_weather()
