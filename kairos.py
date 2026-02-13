import requests
import json
from datetime import datetime

def get_wind_dir(deg):
    if 337.5 <= deg or deg < 22.5: return "Β"
    if 22.5 <= deg < 67.5: return "ΒΑ"
    if 67.5 <= deg < 112.5: return "Α"
    if 112.5 <= deg < 157.5: return "ΝΑ"
    if 157.5 <= deg < 202.5: return "Ν"
    if 202.5 <= deg < 247.5: return "ΝΔ"
    if 247.5 <= deg < 292.5: return "Δ"
    if 292.5 <= deg < 337.5: return "ΒΔ"
    return ""

def get_weather():
    # Συντεταγμένες Γήλοφος
    url = "https://api.open-meteo.com/v1/forecast?latitude=40.00&longitude=21.45&current_weather=true&hourly=surface_pressure,precipitation"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        current = data['current_weather']
        temp = current['temperature']
        wind = current['windspeed']
        wind_deg = current['winddirection']
        wind_dir_text = get_wind_dir(wind_deg)
        
        # Πίεση και Βροχή από τα hourly δεδομένα
        pressure = data['hourly']['surface_pressure'][0]
        rain = data['hourly']['precipitation'][0]

        # Πρόγνωση status βάσει πίεσης
        if pressure <= 1007:
            status = "ΕΠΙΔΕΙΝΩΣΗ"
        elif pressure > 1020:
            status = "ΑΙΘΡΙΟΣ"
        else:
            status = "ΣΥΝΝΕΦΙΑ - ΗΛΙΟΣ"

        # Το πακέτο που πάει στο site
        weather_data = {
            "temperature": temp,
            "humidity": 65,
            "pressure": pressure,
            "wind_speed": wind,
            "wind_dir": wind_dir_text,
            "rain": rain,
            "status": status,
            "last_update": datetime.now().strftime("%H:%M:%S")
        }

        # Γράψιμο στο data.json
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(weather_data, f, ensure_ascii=False, indent=4)
            
        print(f"Ενημερώθηκε! Τελευταία μέτρηση: {temp}°C, {wind_dir_text} {wind}km/h, Βροχή: {rain}mm")

    except Exception as e:
        print(f"Σφάλμα: {e}")

if __name__ == "__main__":
    get_weather()
