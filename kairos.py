import requests
from datetime import datetime
import pytz

# Στοιχεία για Γήλοφο
LAT = 40.0000  
LON = 21.0000
STATION_NAME = "ΓΗΛΟΦΟΣ"

def get_weather():
    # API με αυτόματο timezone
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,is_day,precipitation,rain,showers,snowfall,weather_code,cloud_cover,surface_pressure,wind_speed_10m,wind_direction_10m&timezone=auto"
    
    try:
        response = requests.get(url)
        data = response.json()['current']
        
        temp = data['temperature_2m']
        hum = data['relative_humidity_2m']
        wind_speed = data['wind_speed_10m']
        wind_dir = data['wind_direction_10m']
        pressure = data['surface_pressure']
        clouds = data['cloud_cover']
        is_day = data['is_day']

        # ΑΥΤΟΜΑΤΗ ΩΡΑ ΑΘΗΝΑΣ (Πιάνει και θερινή/χειμερινή)
        athens_tz = pytz.timezone('Europe/Athens')
        athens_time = datetime.now(athens_tz)
        time_str = athens_time.strftime("%H:%M:%S")
        
        # --- ΠΡΟΣΔΙΟΡΙΣΜΟΣ ΚΑΤΕΥΘΥΝΣΗΣ ΑΝΕΜΟΥ ---
        directions = ["ΒΟΡΙΑΣ", "ΒΑ", "ΑΝΑΤΟΛΙΚΟΣ", "ΝΑ", "ΝΟΤΙΑΣ", "ΝΔ", "ΔΥΤΙΚΟΣ", "ΒΔ"]
        idx = int((wind_dir + 22.5) / 45) % 8
        wind_text = directions[idx]

        # --- ΞΕΚΟΚΑΛΙΣΜΑ ΚΑΙ ΔΙΟΡΘΩΣΗ ΑΠΟΚΛΙΣΗΣ ---
        if clouds <= 25:
            weather_desc = "ΛΙΑΚΑΔΑ.ΑΙΘΡΙΟΣ" if is_day else "ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ"
        elif 25 < clouds <= 60:
            if hum < 70:
                weather_desc = "ΛΙΑΚΑΔΑ.ΑΙΘΡΙΟΣ" if is_day else "ΞΑΣΤΕΡΙΑ.ΑΙΘΡΙΟΣ"
            else:
                weather_desc = "ΑΡΑΙΗ ΣΥΝΝΕΦΙΑ"
        else:
            weather_desc = "ΑΡΑΙΗ ΣΥΝΝΕΦΙΑ" if hum < 50 else "ΣΥΝΝΕΦΙΑ"

        # Δημιουργία της σελίδας (HTML)
        html_content = f"""
        <!DOCTYPE html>
        <html lang="el">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="refresh" content="900">
            <title>ΚΑΙΡΟΣ ΓΗΛΟΦΟΥ</title>
            <style>
                body {{ font-family: sans-serif; text-align: center; background: #121212; color: white; padding: 20px; }}
                .container {{ border: 2px solid #444; display: inline-block; padding: 20px; border-radius: 15px; background: #1e1e1e; min-width: 320px; }}
                h1 {{ color: #00acee; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 2px; }}
                .desc {{ font-size: 32px; font-weight: bold; color: #ffcc00; margin: 20px 0; border-bottom: 1px solid #333; padding-bottom: 10px; }}
                .stat {{ font-size: 24px; margin: 10px 0; }}
                .wind-info {{ font-size: 20px; color: #00ffcc; margin-top: 15px; font-weight: bold; background: #2a2a2a; padding: 10px; border-radius: 8px; }}
                .update {{ font-size: 14px; color: #888; margin-top: 20px; font-style: italic; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>{STATION_NAME}</h1>
                <div class="desc">{weather_desc}</div>
                <div class="stat">🌡️ {temp}°C</div>
                <div class="stat">💧 Υγρασία: {hum}%</div>
                <div class="stat">⏲️ Πίεση: {pressure} hPa</div>
                <div class="wind-info">💨 {wind_text} | {wind_speed} km/h ({wind_dir}°)</div>
                <div class="update">Τελευταία ενημέρωση: {time_str} (Ώρα Αθήνας)</div>
            </div>
        </body>
        </html>
        """
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
            
    except Exception as e:
        print(f"Σφάλμα: {e}")

if __name__ == "__main__":
    get_weather()
