from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
import random
from datetime import datetime
import requests  # For making API calls (if using real data sources)

app = Flask(__name__)
CORS(app)


# Mock function to simulate real-time data (replace with actual API calls)
def get_real_time_data(city):
    # Simulate fetching live weather, crime, and traffic data
    weather_conditions = ["Clear", "Rainy", "Stormy", "Extreme Heat"]
    crime_reports = ["Low", "Moderate", "High"]
    traffic_conditions = ["Normal", "Congested", "Accident Reported"]

    return {
        "weather": random.choice(weather_conditions),
        "crime": random.choice(crime_reports),
        "traffic": random.choice(traffic_conditions),
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


# Generate dynamic safety recommendations based on real-time conditions
def get_safety_recommendations(city):
    live_data = get_real_time_data(city)
    alerts = []
    recommendations = []

    # Weather-based alerts & recommendations
    if live_data["weather"] == "Rainy":
        alerts.append(f"Heavy rain expected in {city}. Possible flooding.")
        recommendations.extend([
            "Carry an umbrella or raincoat",
            "Avoid walking through flooded areas",
            "Check for public transport delays"
        ])
    elif live_data["weather"] == "Stormy":
        alerts.append(f"Severe storm warning in {city}. Seek shelter if outdoors.")
        recommendations.extend([
            "Stay indoors if possible",
            "Avoid open areas and tall structures",
            "Charge electronic devices in case of power outages"
        ])

    # Crime-based alerts & recommendations
    if live_data["crime"] == "Moderate":
        alerts.append(f"Moderate crime activity reported in {city}. Stay vigilant.")
        recommendations.extend([
            "Avoid poorly lit areas at night",
            "Keep valuables out of sight",
            "Use trusted transportation services"
        ])
    elif live_data["crime"] == "High":
        alerts.append(f"High crime alert in {city}. Exercise extreme caution.")
        recommendations.extend([
            "Avoid traveling alone at night",
            "Keep emergency contacts handy",
            "Consider altering your travel route"
        ])

    # Traffic-based alerts & recommendations
    if live_data["traffic"] == "Congested":
        alerts.append(f"Heavy traffic reported in {city}.")
        recommendations.extend([
            "Use alternate routes if possible",
            "Check real-time traffic apps before heading out",
            "Allow extra travel time"
        ])
    elif live_data["traffic"] == "Accident Reported":
        alerts.append(f"Accident reported in {city}. Expect delays.")
        recommendations.extend([
            "Avoid the affected area if possible",
            "Follow local traffic advisories",
            "Drive cautiously in the vicinity"
        ])

    # Default recommendations if no specific alerts
    if not alerts:
        alerts.append(f"No major alerts for {city}. Conditions are stable.")
        recommendations.extend([
            "Stay aware of your surroundings",
            "Keep emergency numbers saved",
            "Follow local news for updates"
        ])

    return {
        "city": city,
        "alerts": alerts,
        "recommendations": recommendations,
        "live_data": live_data,
        "timestamp": live_data["last_updated"]
    }


# HTML Template (Updated for Real-Time Display)
TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Travel Safety Bot</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
            color: white;
            min-height: 100vh;
        }
        .alert-box {
            animation: fadeIn 0.8s ease-in-out;
            background: rgba(255, 75, 75, 0.2);
            border-left: 4px solid #ff4b4b;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
        }
        .recommendation-box {
            animation: fadeIn 1s ease-in-out;
            background: rgba(50, 205, 50, 0.2);
            border-left: 4px solid #32cd32;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
        }
        .data-box {
            background: rgba(0, 191, 255, 0.2);
            border-left: 4px solid #00bfff;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .pulse {
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
    </style>
</head>
<body>
    <div class="container py-5">
        <div class="text-center mb-5">
            <h1 class="display-4 mb-3">🌍 Travel Safety Bot</h1>
            <p class="lead">Get real-time safety alerts and recommendations</p>

            <div class="row justify-content-center mt-4">
                <div class="col-md-6">
                    <div class="input-group">
                        <input type="text" id="cityInput" class="form-control form-control-lg" 
                               placeholder="Enter city name" autofocus>
                        <button class="btn btn-warning btn-lg" onclick="checkSafety()">
                            Check Safety
                        </button>
                    </div>
                    <small class="text-light mt-2">Press Enter to search</small>
                </div>
            </div>
        </div>

        <div id="result" class="d-none">
            <div class="row justify-content-center">
                <div class="col-md-8">
                    <h3 class="text-center mb-4" id="cityHeader"></h3>

                    <!-- Live Data Summary -->
                    <div class="data-box mb-4">
                        <h5>📊 Current Conditions:</h5>
                        <div class="row text-center mt-3">
                            <div class="col-md-4">
                                <h6>🌤️ Weather</h6>
                                <p id="weatherData">-</p>
                            </div>
                            <div class="col-md-4">
                                <h6>👮 Crime Level</h6>
                                <p id="crimeData">-</p>
                            </div>
                            <div class="col-md-4">
                                <h6>🚦 Traffic</h6>
                                <p id="trafficData">-</p>
                            </div>
                        </div>
                        <small class="text-muted" id="updateTime"></small>
                    </div>

                    <!-- Alerts -->
                    <div class="alert-box">
                        <h5>⚠️ Active Alerts:</h5>
                        <ul id="alertsList" class="mt-3"></ul>
                    </div>

                    <!-- Recommendations -->
                    <div class="recommendation-box">
                        <h5>🛡️ Recommended Actions:</h5>
                        <ul id="recommendationsList" class="mt-3"></ul>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function checkSafety() {
            const city = document.getElementById('cityInput').value.trim();
            if (!city) {
                alert("Please enter a city name.");
                return;
            }

            fetch(`/api/safety?city=${encodeURIComponent(city)}`)
                .then(response => response.json())
                .then(data => {
                    // Update city header
                    document.getElementById('cityHeader').textContent = `Safety Report for ${data.city}`;

                    // Update live data
                    document.getElementById('weatherData').textContent = data.live_data.weather;
                    document.getElementById('crimeData').textContent = data.live_data.crime;
                    document.getElementById('trafficData').textContent = data.live_data.traffic;
                    document.getElementById('updateTime').textContent = `Last updated: ${data.timestamp}`;

                    // Update alerts
                    const alertsList = document.getElementById('alertsList');
                    alertsList.innerHTML = data.alerts.map(alert => 
                        `<li class="mb-2">${alert}</li>`
                    ).join('');

                    // Update recommendations
                    const recList = document.getElementById('recommendationsList');
                    recList.innerHTML = data.recommendations.map(rec => 
                        `<li class="mb-2">${rec}</li>`
                    ).join('');

                    // Show results
                    document.getElementById('result').classList.remove('d-none');
                })
                .catch(error => {
                    console.error("Error:", error);
                    alert("Could not fetch safety data. Please try again.");
                });
        }

        // Allow Enter key to trigger search
        document.getElementById('cityInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') checkSafety();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(TEMPLATE)

@app.route('/api/safety')
def safety():
    city = request.args.get('city', 'Unknown')
    return jsonify(get_safety_recommendations(city))

if __name__ == '__main__':
    app.run(debug=True)
