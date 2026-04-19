# 🎓 Smart Campus AI Assistant

**Smart Campus AI Assistant** is a lightweight, offline-ready web application designed for low-connectivity environments. Built with Flask and modern web technologies, it provides intelligent interaction for students and visitors without requiring heavy external dependencies or cloud databases.

## 🚀 Features
- **Intelligent AI Chat**: Get instant answers about library timings, canteen specials, lab locations, and more using an efficient keyword-matching NLP engine.
- **QR-Based Physical Interaction**: Simulated QR scan buttons (Library, Lab, Canteen) provide location-specific contextual information.
- **Voice Intelligence**: Hands-free interaction using browser-based Speech-to-Text.
- **Offline-First Design**: All data is stored in local JSON files, ensuring performance even with poor internet connectivity.
- **Activity Logging**: Comprehensive interaction tracking in `logs.json`.
- **Premium UI**: Modern dark-themed, glassmorphic interface designed for clarity and speed.

## 🛠️ Tech Stack
- **Backend**: Python 3.x + Flask
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript (ES6)
- **Data Storage**: JSON-based flat files (No SQL/NoSQL DB required)
- **NLP**: Static keyword frequency matching

## 📋 Approach
- **Efficiency**: The entire project is under 1MB, optimized for rapid deployment and accessibility.
- **Low Connectivity focus**: By utilizing local JSON and static files, the app remains functional in dead zones or high-traffic areas where cellular data is unreliable.
- **Simulated Physical Layer**: The "QR Simulation" allows developers to test location-based triggers within the browser.

## ⚙️ How it Works
1. **User Query**: The user types or speaks a query.
2. **Backend Analysis**: Flask processes the query by checking it against the `knowledge_base` in `campus_data.json`.
3. **Response Generation**: The most relevant response is logged and returned to the frontend.
4. **Contextual Scans**: Physical interactions are mirrored by the system-level simulation points.

## 🏠 Setup Instructions
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python app.py
   ```
3. Open `http://127.0.0.1:5000` in your browser.

---
*Designed for the modern campus experience. Hackathon-ready and fully extensible.*
