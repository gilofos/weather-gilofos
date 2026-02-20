import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup

def get_weather():
    # 1. Scraping από kairosradar.gr για την κατάσταση
    status_text = "ΣΥΝΝΕΦΙΑ / ΑΙΘΡΙΟΣ"
    try:
        r = requests.get("https://www.kairosradar.gr/", timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        radar_raw = soup.find("div", {"class": "current-condition"}).text.strip()
        
        # Εφαρμογή του κανόνα σου για ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ
        if "Αίθριος" in radar_raw or "Καθαρός" in radar_raw:
            status_text = "ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ"
        else:
            status_text = radar_raw.upper()
    except:
        pass

    # 2. Δεδομένα από Open-Meteo
    try:
        api = "https://api.open-meteo.com/v1/forecast?latitude=40.0125&longitude=21.4625&current=temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,wind_direction_10m&timezone=Europe%2FAthens"
        res = requests.get(api).json()['current']
        
        # Υπολογισμός κατεύθυνσης ανέμου
        d = res['wind_direction_10m']
        if 337.5 <= d or d < 22.5: txt = "ΒΟΡΕΙΟΣ"
        elif 22.5 <= d < 67.5: txt = "ΒΑ"
        elif 67.5 <= d < 112.5: txt = "ΑΝΑΤΟΛΙΚΟΣ"
        elif 112.5 <= d < 157.5: txt = "ΝΑ"
        elif 157.5 <= d < 202.5: txt = "ΝΟΤΙΟΣ"
        elif 202.5 <= d < 247.5: txt = "ΝΔ"
        elif 247.5 <= d < 292.5: txt = "ΔΥΤΙΚΟΣ"
        else: txt = "ΒΔ"

        # 3. Το αρχείο data.json με τα ονόματα που θέλει η σελίδα σου
        # ΠΡΟΣΟΧΗ: Εδώ χρησιμοποιούμε τα ονόματα που ήδη ξέρει το site σου
        data = {
            "temperature": f"{round(res['temperature_2m'])}°C",
            "humidity": f"{res['relative_humidity_2m']}%",
            "pressure": f"{round(res['surface_pressure'])} hPa",
            "wind_speed": f"{round(res['wind_speed_10m'])} km/h",
            "wind_deg": f"{d}°",
            "wind_full": f"{txt} ({d}°) {round(res['wind_speed_10m'])} km/h",
            "status": status_text,
            "last_update": datetime.now().strftime("%H:%M:%S")
        }
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("Success!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_weather()
