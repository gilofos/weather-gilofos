import requests
import json
from datetime import datetime

# Ρυθμίσεις
API_KEY = "36c53e0281b3749726207f2323f40332" 
CITY = "Gilofos,GR"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=el"

try:
    response = requests.get(URL)
    data = response.json()

    weather_data = {
        "temperature": round(data["main"]["temp"]),
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"],
        "last_update": datetime.now().strftime("%d/%m/%Y %H:%M")
    }

    # Αποθήκευση σε JSON (για το ιστορικό σου)
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(weather_data, f, ensure_ascii=False)

    # ΦΤΙΑΧΝΟΥΜΕ ΤΟ WIDGET ΜΕ ΤΟ "ΧΕΡΑΚΙ" (LINK)
    html_content = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ 
                margin: 0; padding: 0; font-family: 'Arial', sans-serif; 
                background: #121212; color: white; text-align: center;
                display: flex; justify-content: center; align-items: center;
                height: 100vh; overflow: hidden;
            }}
            .main-link {{
                text-decoration: none; color: inherit; cursor: pointer;
                display: block; width: 100%; height: 100%; padding: 15px;
            }}
            .header {{ color: #2ecc71; font-size: 14px; font-weight: bold; margin-bottom: 5px; }}
            .title {{ color: #f1c40f; font-size: 20px; font-weight: bold; margin-bottom: 10px; }}
            .clock-box {{ 
                background: #1a1a1a; border-radius: 15px; border: 1px solid #333; 
                padding: 15px; margin-bottom: 10px;
            }}
            .temp {{ font-size: 60px; font-weight: bold; line-height: 1; }}
            .desc {{ color: #aaa; font-size: 16px; text-transform: uppercase; margin-top: 5px; }}
            .extra {{ font-size: 20px; margin: 10px 0; }}
            .details {{ 
                background: #f1c40f; color: black; font-weight: bold; 
                padding: 8px; font-size: 13px; position: absolute; bottom: 0; width: 100%;
            }}
            img {{ width: 80px; }}
        </style>
    </head>
    <body>
        <a href="https://gilofos.github.io/weather-gilofos/" target="_blank" class="main-link">
            <div class="header">● ΣΤΑΘΜΟΣ ΣΕ ΛΕΙΤΟΥΡΓΙΑ</div>
            <div class="title">ΓΗΛΟΦΟΣ ΓΡΕΒΕΝΩΝ</div>
            <div class="clock-box">
                <img src="https://openweathermap.org/img/wn/{weather_data['icon']}@2x.png">
                <div class="temp">{weather_data['temperature']}°C</div>
                <div class="desc">{weather_data['description']}</div>
            </div>
            <div class="extra">💧 Υγρασία: {weather_data['humidity']}%</div>
            <div class="details">ΤΡΕΧΟΥΣΕΣ ΣΥΝΘΗΚΕΣ: {weather_data['last_update']}</div>
        </a>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Επιτυχής ενημέρωση!")

except Exception as e:
    print(f"Σφάλμα: {e}")

        


