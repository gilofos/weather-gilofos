import requests, json
from datetime import datetime

# Ρυθμίσεις για Γήλοφο
LAT, LON = 40.06, 21.80
URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,pressure_msl,wind_speed_10m,weather_code&timezone=auto"

def get_weather():
    try:
        r = requests.get(URL, timeout=10)
        if r.status_code == 200:
            d = r.json()["current"]
            p = round(d["pressure_msl"], 1)
            w = round(d["wind_speed_10m"], 1)
            
            # Λογική Alert - Πάντα θα έχει μια τιμή
            if p < 1000 or w > 50:
                alert = "🚨 ALERT: Επικίνδυνη Κακοκαιρία!"
            elif p < 1007:
                alert = "⚠️ ΠΡΟΣΟΧΗ: Πτώση πίεσης - Καιρός άστατος"
            elif p > 1025:
                alert = "☀️ Καλοκαιρία - Υψηλή πίεση"
            else:
                alert = "✅ Καιρός Σταθερός"

            weather_data = {
                "temp": round(d["temperature_2m"], 1),
                "press": p,
                "wind": w,
                "alert": alert,
                "time": datetime.now().strftime("%H:%M:%S")
            }

            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(weather_data, f, ensure_ascii=False, indent=4)
            print(f"Ενημερώθηκε επιτυχώς στις {weather_data['time']}")
    except Exception as e:
        print(f"Σφάλμα API: {e}")

if __name__ == "__main__":
    get_weather()
