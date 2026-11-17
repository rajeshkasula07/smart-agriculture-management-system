from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

# Enhanced sensor database supporting all layout elements
sensor_database = {
    "node_id": "ESP32_FIELD_01",
    "temperature": 28.0,
    "humidity": 65.0,
    "soil_moisture": 32.0,
    "water_level": 72.0,
    "irrigation_status": "OFF",
    "mode": "AUTOMATIC",
    "alerts": [
        "System initialized successfully",
        "Sensors operating normally"
    ],
    "last_updated": str(datetime.datetime.now())
}

@app.route('/')
def home():
    return jsonify({
        "system": "Smart Agriculture Management System API",
        "status": "Active"
    })

@app.route('/api/telemetry', methods=['GET', 'POST'])
def handle_telemetry():
    global sensor_database
    if request.method == 'POST':
        data = request.json
        sensor_database['temperature'] = data.get('temperature', sensor_database['temperature'])
        sensor_database['humidity'] = data.get('humidity', sensor_database['humidity'])
        sensor_database['soil_moisture'] = data.get('soil_moisture', sensor_database['soil_moisture'])
        sensor_database['water_level'] = data.get('water_level', sensor_database['water_level'])
        
        # Automatic irrigation logic
        if sensor_database['mode'] == "AUTOMATIC":
            if sensor_database['soil_moisture'] < 35.0:
                if sensor_database['irrigation_status'] == "OFF":
                    sensor_database['alerts'].insert(0, "Irrigation started automatically (Low Moisture)")
                sensor_database['irrigation_status'] = "ON"
            else:
                if sensor_database['irrigation_status'] == "ON":
                    sensor_database['alerts'].insert(0, "Moisture optimal. Irrigation stopped.")
                sensor_database['irrigation_status'] = "OFF"
        
        # Keep only the latest 4 alerts
        sensor_database['alerts'] = sensor_database['alerts'][:4]
        sensor_database['last_updated'] = str(datetime.datetime.now())
        return jsonify({"status": "success", "data": sensor_database})
    
    return jsonify(sensor_database)

@app.route('/api/control-valve', methods=['POST'])
def control_valve():
    global sensor_database
    data = request.json
    action = data.get('action') # 'ON' or 'OFF'
    if action in ['ON', 'OFF']:
        sensor_database['irrigation_status'] = action
        sensor_database['mode'] = "MANUAL"
        sensor_database['alerts'].insert(0, f"Manual override: Pump turned {action}")
        sensor_database['alerts'] = sensor_database['alerts'][:4]
        sensor_database['last_updated'] = str(datetime.datetime.now())
        return jsonify({"success": True, "data": sensor_database})
    return jsonify({"success": False, "error": "Invalid action"}), 400

@app.route('/api/set-mode', methods=['POST'])
def set_mode():
    global sensor_database
    data = request.json
    mode = data.get('mode') # 'AUTOMATIC' or 'MANUAL'
    if mode in ['AUTOMATIC', 'MANUAL']:
        sensor_database['mode'] = mode
        sensor_database['alerts'].insert(0, f"System switched to {mode} mode")
        sensor_database['alerts'] = sensor_database['alerts'][:4]
        return jsonify({"success": True, "data": sensor_database})
    return jsonify({"success": False, "error": "Invalid mode"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)