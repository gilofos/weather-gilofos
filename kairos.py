import requests
import json
from datetime import datetime

# Ρυθμίσεις
API_KEY = "ΣΥΜΠΛΗΡΩΣΕ_ΤΟ_ΔΙΚΟ_ΣΟΥ_KEY" 
CITY = "Gilofos,GR"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

try:
    response = requests.get(URL)
    data = response.json()

    weather_data = {
        "temperature": round(data["main"]["temp"]),
        "humidity": data["main"]["humidity"],
        "last_update": datetime.now().strftime("%d/%m/%Y %H:%M")
    }

    # Αποθήκευση σε JSON (για το ιστορικό)
    with open("data.json", "w") as f:
        json.dump(weather_data, f)

    # ΦΤΙΑΧΝΟΥΜΕ ΜΙΑ ΜΙΚΡΗ ΣΕΛΙΔΑ (Widget)
    html_content = f"""
    <html>
    <head><meta charset="utf-8"></head>
    <body style="margin:0; padding:0; font-family:sans-serif; text-align:center; background:white;">
        <div style="color:#d9534f; font-size:28px; font-weight:bold;">{weather_data['temperature']}°C</div>
        <div style="color:#555; font-size:16px;">💧 {weather_data['humidity']}%</div>
        <div style="color:#888; font-size:11px; margin-top:5px;">{weather_data['last_update']}</div>
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

except Exception as e:
    print(f"Error: {e}")
       
