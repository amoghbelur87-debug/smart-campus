from flask import Flask, render_template, jsonify, request
import json
import os
import random
import time
from datetime import datetime

app = Flask(__name__)

DATA_FILE = 'campus_data.json'
LOGS_FILE = 'logs.json'

def load_json(filepath):
    # Basic protection against empty/missing files
    if not os.path.exists(filepath):
        return {} if 'campus' in filepath else []
    
    # Retry logic for Windows file locks
    for _ in range(3):
        try:
            with open(filepath, 'r') as f:
                content = f.read().strip()
                if not content:
                    return {} if 'campus' in filepath else []
                return json.loads(content)
        except (json.JSONDecodeError, IOError):
            time.sleep(0.1)
    return {} if 'campus' in filepath else []

def save_json(filepath, data):
    for _ in range(3):
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
                return True
        except IOError:
            time.sleep(0.1)
    return False

def log_interaction(event_type, details, response):
    logs = load_json(LOGS_FILE)
    if not isinstance(logs, list): logs = []
    logs.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": event_type,
        "details": details,
        "response": response
    })
    save_json(LOGS_FILE, logs)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/sensors')
def get_sensors():
    data = load_json(DATA_FILE)
    # Safe defaults to prevent KeyError
    sensors = data.get('sensors', {
        "temperature": 22.0,
        "occupancy": 50,
        "energy": 1.0,
        "status": "Healthy"
    })
    
    # Simulate fluctuations safely
    try:
        sensors['temperature'] = round(sensors.get('temperature', 22.0) + random.uniform(-0.5, 0.5), 1)
        sensors['occupancy'] = max(0, min(100, sensors.get('occupancy', 50) + random.randint(-2, 2)))
        sensors['energy'] = round(sensors.get('energy', 1.0) + random.uniform(-0.1, 0.1), 1)
    except Exception:
        pass # Fallback to existing values
        
    data['sensors'] = sensors
    save_json(DATA_FILE, data)
    return jsonify(sensors)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('query', '').lower()
    data = load_json(DATA_FILE)
    kb = data.get('knowledge_base', {})
    
    response_text = data.get('default_response', "I'm not sure about that.")
    
    for keyword, answer in kb.items():
        if keyword in user_input:
            response_text = answer
            break
            
    log_interaction("CHAT", user_input, response_text)
    return jsonify({"response": response_text})

@app.route('/scan', methods=['POST'])
def scan():
    location = request.json.get('location', '')
    data = load_json(DATA_FILE)
    qr_data = data.get('qr_locations', {}).get(location)
    
    if qr_data:
        response_text = f"📍 {qr_data['info']} | Status: {qr_data['status']}"
    else:
        response_text = "Invalid QR code simulation."
        
    log_interaction("QR_SCAN", location, response_text)
    return jsonify({"response": response_text})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
