import requests
import random
import time

URL = "http://localhost:5000/api/telemetry"

print("Starting Enhanced Virtual ESP32 IoT Node...")
while True:
    payload = {
        "temperature": round(random.uniform(25.0, 35.0), 1),
        "humidity": round(random.uniform(55.0, 80.0), 1),
        "soil_moisture": round(random.uniform(20.0, 50.0), 1), # Drops low to trigger auto irrigation
        "water_level": round(random.uniform(60.0, 95.0), 1)
    }
    
    try:
        response = requests.post(URL, json=payload)
        res_data = response.json()['data']
        print(f"Sent -> Moisture: {payload['soil_moisture']}% | Pump: {res_data['irrigation_status']} | Mode: {res_data['mode']}")
    except Exception as e:
        print("Server offline, retrying...")
        
    time.sleep(4)