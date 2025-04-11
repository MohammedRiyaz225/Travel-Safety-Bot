from flask import Flask, render_template, request, jsonify
import random
from datetime import datetime

app = Flask(__name__)


# Create a simple index.html template
@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Travel Safety Bot</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { padding: 20px; background-color: #f8f9fa; }
            .card { margin-bottom: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
            .alert-high { background-color: #f8d7da; }
            .alert-medium { background-color: #fff3cd; }
            .alert-low { background-color: #d1ecf1; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="mb-4 text-center">Travel Safety Bot</h1>

            <div class="row">
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-header bg-primary text-white">
                            <h5>Search Location</h5>
                        </div>
                        <div class="card-body">
                            <form id="searchForm">
                                <div class="mb-3">
                                    <label for="country" class="form-label">Country</label>
                                    <input type="text" class="form-control" id="country" required>
                                </div>
                                <div class="mb-3">
                                    <label for="city" class="form-label">City (Optional)</label>
                                    <input type="text" class="form-control" id="city">
                                </div>
                                <button type="submit" class="btn btn-primary">Get Safety Alerts</button>
                            </form>
                        </div>
                    </div>

                    <div class="card">
                        <div class="card-header bg-primary text-white">
                            <h5>Alert Preferences</h5>
                        </div>
                        <div class="card-body">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="weatherAlerts" checked>
                                <label class="form-check-label" for="weatherAlerts">Weather Alerts</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="travelAdvisories" checked>
                                <label class="form-check-label" for="travelAdvisories">Travel Advisories</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="localIncidents" checked>
                                <label class="form-check-label" for="localIncidents">Local Incidents</label>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="col-md-8">
                    <div class="card">
                        <div class="card-header bg-primary text-white">
                            <h5>Safety Alerts</h5>
                        </div>
                        <div class="card-body">
                            <div id="alertsContainer">
                                <div class="alert alert-info">
                                    Search for a location to see safety alerts.
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            document.getElementById('searchForm').addEventListener('submit', function(e) {
                e.preventDefault();

                const country = document.getElementById('country').value;
                const city = document.getElementById('city').value;
                const weatherChecked = document.getElementById('weatherAlerts').checked;
                const advisoryChecked = document.getElementById('travelAdvisories').checked;
                const incidentsChecked = document.getElementById('localIncidents').checked;

                fetch('/api/alerts', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        country: country,
                        city: city,
                        filters: {
                            weather: weatherChecked,
                            advisory: advisoryChecked,
                            incident: incidentsChecked
                        }
                    }),
                })
                .then(response => response.json())
                .then(data => {
                    const alertsContainer = document.getElementById('alertsContainer');

                    if (data.alerts.length === 0) {
                        alertsContainer.innerHTML = '<div class="alert alert-info">No alerts found for this location with current filters.</div>';
                        return;
                    }

                    let alertsHTML = '';
                    data.alerts.forEach(alert => {
                        alertsHTML += `
                            <div class="alert alert-${alert.severity} mb-3">
                                <div class="d-flex justify-content-between">
                                    <strong>${alert.title}</strong>
                                    <span class="badge bg-${getSeverityBadge(alert.severity)}">${alert.severity.toUpperCase()}</span>
                                </div>
                                <p class="mb-0 mt-2">${alert.description}</p>
                                <small class="text-muted">Type: ${alert.type} | Issued: ${alert.timestamp}</small>
                            </div>
                        `;
                    });

                    alertsContainer.innerHTML = alertsHTML;
                })
                .catch(error => {
                    console.error('Error:', error);
                    alertsContainer.innerHTML = '<div class="alert alert-danger">Error fetching alerts. Please try again.</div>';
                });
            });

            function getSeverityBadge(severity) {
                switch(severity) {
                    case 'high': return 'danger';
                    case 'medium': return 'warning';
                    case 'low': return 'info';
                    default: return 'secondary';
                }
            }
        </script>
    </body>
    </html>
    '''


# API endpoint to get safety alerts
@app.route('/api/alerts', methods=['POST'])
def get_alerts():
    data = request.json
    country = data.get('country', '')
    city = data.get('city', '')
    filters = data.get('filters', {})

    # Generate sample alerts
    all_alerts = []

    # Add weather alerts if enabled
    if filters.get('weather', True):
        weather_alerts = [
            {
                'type': 'weather',
                'severity': random.choice(['low', 'medium', 'high']),
                'title': f'Weather Alert for {country}',
                'description': f'Potential storms in {country} area. Stay informed about changing conditions.',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            {
                'type': 'weather',
                'severity': 'medium',
                'title': 'Temperature Warning',
                'description': f'Unusual temperatures expected in {country}. Plan accordingly.',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
        ]
        all_alerts.extend(weather_alerts)

    # Add travel advisories if enabled
    if filters.get('advisory', True):
        travel_alerts = [
            {
                'type': 'advisory',
                'severity': random.choice(['medium', 'high']),
                'title': f'Travel Advisory for {country}',
                'description': f'Exercise increased caution when traveling to {city if city else country}.',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            {
                'type': 'advisory',
                'severity': 'low',
                'title': 'Entry Requirements Updated',
                'description': f'Check latest visa requirements for {country} before traveling.',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
        ]
        all_alerts.extend(travel_alerts)

    # Add local incidents if enabled
    if filters.get('incident', True):
        incident_alerts = [
            {
                'type': 'incident',
                'severity': random.choice(['low', 'medium']),
                'title': f'Local Event in {city if city else country}',
                'description': f'Large public gathering scheduled. Expect increased crowds and possible traffic disruptions.',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
        ]
        all_alerts.extend(incident_alerts)

    # Randomly select a subset of alerts to show
    if all_alerts:
        selected_alerts = random.sample(all_alerts, min(len(all_alerts), 4))
    else:
        selected_alerts = []

    return jsonify({'alerts': selected_alerts})


if __name__ == '__main__':
    app.run(debug=True)