import requests
import json
from datetime import datetime

# Ρυθμίσεις (Γήλοφος)
API_KEY = "36c53e0281b3749726207f2323f40332"
LAT = 40.0632
LON = 21.8025
URL = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric&lang=el"

def get_moon_phase(date):
    """Υπολογίζει τη φάση της σελήνης (0=Νέα, 4=Πανσέληνος)"""
    diff = date - datetime(2001, 1, 1)
    days = diff.days + diff.seconds / 86400.0
    lunation = (days - 2.48) % 29.530588853
    phase_idx = int((lunation / 29.53) * 8)
    phases = ["Νέα Σελήνη", "Αύξων Μηνίσκος", "Πρώτο Τέταρτο", "Αύξων Αμφίκυρτος", 
              "Πανσέληνος", "Φθίνων Αμφίκυρτος", "Τελευταίο Τέταρτο", "Φθίνων Μηνίσκος"]
    return phases[phase_idx]

try:
    response = requests.get(URL)
    data = response.json()

    now = datetime.now()
    sunrise = datetime.fromtimestamp(data["sys"]["sunrise"])
    sunset = datetime.fromtimestamp(data["sys"]["sunset"])
    
    # Έλεγχος αν είναι Μέρα ή Νύχτα
    is_day = sunrise < now < sunset

    weather_data = {
        "temp": round(data["main"]["temp"], 1),
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "description": data["weather"][0]["description"].capitalize(),
        "icon": data["weather"][0]["icon"],
        "is_day": is_day,
        "moon_phase": get_moon_phase(now),
        "sunrise": sunrise.strftime("%H:%M"),
        "sunset": sunset.strftime("%H:%M"),
        "last_update": now.strftime("%d/%m/%Y %H:%M")
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(weather_data, f, ensure_ascii=False, indent=4)

    print(f"Επιτυχής ενημέρωση για το Γήλοφο!")
    print(f"Κατάσταση: {'Μέρα' if is_day else 'Νύχτα'}, Σελήνη: {weather_data['moon_phase']}")

except Exception as e:
    print(f"Σφάλμα: {e}")

