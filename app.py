from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import threading
import os

# Mock modules to replace the actual implementations for this example
class APIHandler:
    def __init__(self, default_city="London", units="metric", api_key=""):
        self.default_city = default_city
        self.units = units
        self.api_key = api_key
    
    def fetch_weather(self):
        # Mock weather data
        return {
            "name": self.default_city,
            "main": {
                "temp": 23.5,
                "feels_like": 25.1,
                "temp_min": 20.0,
                "temp_max": 26.0,
                "humidity": 65,
                "pressure": 1012
            },
            "wind": {"speed": 3.5, "deg": 180},
            "sys": {"sunrise": 1689390000, "sunset": 1689440000},
            "weather": [{"description": "clear sky", "icon": "01d"}]
        }
    
    def fetch_forecast(self):
        # Mock forecast data
        return {
            "list": [
                {
                    "dt_txt": "2023-07-15 12:00:00",
                    "main": {"temp": 24.0, "humidity": 60},
                    "weather": [{"description": "sunny", "icon": "01d"}],
                    "wind": {"speed": 2.5}
                },
                # More forecast items would be here in a real implementation
            ]
        }

def parse_current(data):
    if not data or 'main' not in data or 'weather' not in data:
        return {}
    
    return {
        "city": data.get("name", "-"),
        "temp": data["main"].get("temp", "-"),
        "feels_like": data["main"].get("feels_like", "-"),
        "temp_min": data["main"].get("temp_min", "-"),
        "temp_max": data["main"].get("temp_max", "-"),
        "humidity": data["main"].get("humidity", "-"),
        "wind_speed": data.get("wind", {}).get("speed", "-"),
        "wind_deg": data.get("wind", {}).get("deg", "-"),
        "pressure": data["main"].get("pressure", "-"),
        "sunrise": data.get("sys", {}).get("sunrise", "-"),
        "sunset": data.get("sys", {}).get("sunset", "-"),
        "description": data["weather"][0].get("description", "-"),
        "icon": data["weather"][0].get("icon", None),
    }

def parse_summary(data):
    if not data or 'list' not in data:
        return []
    
    summaries = []
    for item in data['list']:
        main = item['main']
        weather = item['weather'][0]
        summaries.append({
            "date": item['dt_txt'],
            "temperature": main.get('temp'),
            "humidity": main.get('humidity'),
            "description": weather.get('description'),
            "wind_speed": item.get('wind', {}).get('speed', '-')
        })
    
    return summaries

def load_config():
    # In a real app, this would load from a file
    return {
        "location": "London",
        "units": "metric",
        "api_key": "your_api_key_here",
        "favorites": ["London", "Paris"]
    }

def save_config(config):
    # In a real app, this would save to a file
    pass

# Actual Flask app starts here
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Thread-safe config handling
config = load_config()
config_lock = threading.Lock()

def get_api_handler(city=None, units=None):
    """Create an APIHandler instance with current configuration"""
    with config_lock:
        current_config = config.copy()
    
    target_city = city or current_config.get("location", "London")
    target_units = units or current_config.get("units", "metric")
    api_key = current_config.get("api_key")
    
    return APIHandler(
        default_city=target_city,
        units=target_units,
        api_key=api_key
    )

@app.route('/', methods=['GET'])
def home():
    try:
        city = request.args.get('city', '').strip() or config.get('location', 'London')
        api = get_api_handler(city=city)
        data = api.fetch_weather()
        
        if not data:
            flash("Failed to fetch weather data. Please try again later.", "danger")
            return render_template('home.html', weather=None)
        
        weather = parse_current(data)
        if not weather:
            flash("Failed to parse weather data. Please try again later.", "danger")
            return render_template('home.html', weather=None)
        
        # Convert timestamps to readable times
        if weather.get('sunrise') != '-':
            weather['sunrise'] = datetime.utcfromtimestamp(weather['sunrise']).strftime('%H:%M')
        if weather.get('sunset') != '-':
            weather['sunset'] = datetime.utcfromtimestamp(weather['sunset']).strftime('%H:%M')
            
        return render_template('home.html', weather=weather)
    
    except Exception as e:
        flash(f"An unexpected error occurred: {str(e)}", "danger")
        return render_template('home.html', weather=None)

@app.route('/search', methods=['POST'])
def search():
    city = request.form.get('city', '').strip()
    if not city:
        flash("Please enter a city name", "warning")
        return redirect(url_for('home'))
    
    return redirect(url_for('home', city=city))

@app.route('/favorites')
def favorites():
    with config_lock:
        favs = config.get('favorites', [])
    
    weather_list = []
    for city in favs:
        try:
            api = get_api_handler(city=city)
            data = api.fetch_weather()
            if data:
                weather = parse_current(data)
                if weather:
                    weather_list.append({
                        "city": city,
                        "temperature": weather.get("temp", "-"),
                        "description": weather.get("description", "-"),
                        "icon": weather.get("icon", None)
                    })
        except Exception:
            continue  # Skip this city if there's an error
    
    return render_template('favorites.html', weather_list=weather_list)

@app.route('/add_favorite', methods=['POST'])
def add_favorite():
    city = request.form.get('city', '').strip()
    if not city:
        flash("No city specified to add to favorites", "warning")
        return redirect(url_for('home'))
    
    with config_lock:
        if 'favorites' not in config:
            config['favorites'] = []
            
        if city not in config['favorites']:
            config['favorites'].append(city)
            save_config(config)
            flash(f"Added {city} to favorites!", "success")
        else:
            flash(f"{city} is already in your favorites", "info")
    
    return redirect(url_for('home', city=city))

@app.route('/remove_favorite/<city>')
def remove_favorite(city):
    with config_lock:
        if 'favorites' in config and city in config['favorites']:
            config['favorites'].remove(city)
            save_config(config)
            flash(f"Removed {city} from favorites", "success")
        else:
            flash(f"{city} was not in your favorites", "warning")
    
    return redirect(url_for('favorites'))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        new_city = request.form.get('default_city', '').strip()
        new_units = request.form.get('units', 'metric')
        
        if not new_city:
            flash("Default city cannot be empty", "danger")
            return redirect(url_for('settings'))
        
        with config_lock:
            config['location'] = new_city
            config['units'] = new_units
            save_config(config)
        
        flash("Settings updated successfully!", "success")
        return redirect(url_for('home'))
    
    with config_lock:
        settings_data = {
            'default_city': config.get('location', 'London'),
            'units': config.get('units', 'metric')
        }
    
    return render_template('settings.html', config=settings_data)

@app.route('/forecast')
def forecast():
    city = request.args.get('city', '').strip() or config.get('location', 'London')
    
    try:
        api = get_api_handler(city=city)
        data = api.fetch_forecast()
        
        if not data or 'list' not in data:
            flash(f"Forecast data not available for {city}", "warning")
            return redirect(url_for('home'))
        
        summaries = parse_summary(data)
        if not summaries:
            flash(f"Failed to parse forecast data for {city}", "warning")
            return redirect(url_for('home'))
        
        # Format dates for better display
        for summary in summaries:
            try:
                dt = datetime.strptime(summary['date'], "%Y-%m-%d %H:%M:%S")
                summary['date'] = dt.strftime("%a, %b %d %H:%M")
            except (ValueError, TypeError):
                pass  # Keep original format
        
        return render_template('forecast.html', city=city, forecast=summaries)
    
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)