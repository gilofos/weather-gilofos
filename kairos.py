import requests
import json

# Ρυθμίσεις για Γηλόφο
API_KEY = "154abadcd6dbf332847ef2f672a9793c"
LAT = 40.0632 
LON = 21.8025

def get_weather():
    try:
        # Κλήση στο OpenWeather για τον Γηλόφο
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric&lang=el"
        response = requests.get(url)
        data = response.json()
        
        # Οργάνωση των δεδομένων που θα στείλουμε στο site
        weather_data = {
            "temp": round(data["main"]["temp"], 1),
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "description": data["weather"][0]["description"].capitalize(),
            "city": "Γηλόφος",
            "timestamp": data["dt"]
        }
        
        # Δημιουργία/Ενημέρωση του αρχείου data.json
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(weather_data, f, ensure_ascii=False, indent=4)
            
        print("Επιτυχία! Το data.json ενημερώθηκε με τα νέα στοιχεία.")
        
    except Exception as e:
        print(f"Κάτι πήγε στραβά: {e}")

if __name__ == "__main__":
    get_weather()