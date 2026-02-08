import requests
import json
from datetime import datetime

# Ρυθμίσεις για τον Γήλοφο
LAT, LON = 40.06, 21.80
OFFSET = 119 # Για να βγάζει 1009 hPa

URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m&timezone=auto"

def update():
    try:
        r = requests.get(URL, timeout=10)
        if r.status_code == 200:
            data = r.json()["current"]
            p_final = int(data["surface_pressure"] + OFFSET)
            
            # ΤΑ ΚΛΕΙΔΙΑ ΠΟΥ ΠΡΕΠΕΙ ΝΑ ΕΙΝΑΙ ΙΔΙΑ ΜΕ ΤΟ HTML
            out = {
                "temp": round(data["temperature_2m"], 1),
                "hum": data["relative_humidity_2m"],
                "pres": p_final,
                "wind": round(data["wind_speed_10m"], 1),
                "alert": True if (p_final < 1000 or data["wind_speed_10m"] > 35) else False
            }
            
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(out, f, indent=4)
            print(f"OK: {p_final} hPa")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update()
