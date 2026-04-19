from flask import Flask, render_template, jsonify, request
import json
import os
import random
from datetime import datetime

app = Flask(__name__)

DATA_FILE = 'campus_data.json'
LOGS_FILE = 'logs.json'

def load_json(filepath):
    if not os.path.exists(filepath):
        return {} if 'data' in filepath else []
    with open(filepath, 'r') as f:
        try:
            return json.load(f)
        except:
            return {} if 'data' in filepath else []

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def log_interaction(event_type, details, response):
    logs = load_json(LOGS_FILE)
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
    # Simulate slight fluctuation in sensors
    sensors = data.get('sensors', {})
    sensors['temperature'] = round(22 + random.uniform(-2, 2), 1)
    sensors['occupancy'] = max(0, min(100, sensors['occupancy'] + random.randint(-5, 5)))
    sensors['energy'] = round(1.2 + random.uniform(-0.3, 0.3), 1)
    
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
