import requests
from datetime import datetime

# Στοιχεία για Γήλοφο
LAT = 40.0000  
LON = 21.0000
STATION_NAME = "ΓΗΛΟΦΟΣ"

def get_weather():
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

        # ΩΡΑ UTC (ΑΚΡΙΒΩΣ ΟΠΩΣ ΧΘΕΣ)
        time_str = datetime.utcnow().strftime("%H:%M:%S")

        # --- ΚΑΤΑΣΤΑΣΗ ΚΑΙΡΟΥ ---
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
                .container {{ border: 2px solid #444; display: inline-block; padding: 20px; border-radius: 15px; background: #1e1e1e; }}
                h1 {{ color: #00acee; margin-bottom: 5px; }}
                .stat {{ font-size: 24px; margin: 10px 0; }}
                .desc {{ font-size: 28px; font-weight: bold; color: #ffcc00; margin: 20px 0; }}
                .wind-info {{ font-size: 18px; color: #aaa; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>{STATION_NAME}</h1>
                <div class="desc">{weather_desc}</div>
                <div class="stat">Θερμοκρασία: {temp}°C</div>
                <div class="stat">Υγρασία: {hum}%</div>
                <div class="stat">Πίεση: {pressure} hPa</div>
                <div class="wind-info">Άνεμος: {wind_speed} km/h | Κατεύθυνση: {wind_dir}°</div>
                <hr>
                <div style="font-size: 14px; color: #888;">Τελευταία ενημέρωση (UTC): {time_str}</div>
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
