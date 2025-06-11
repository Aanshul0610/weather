from flask import Flask, render_template, request, redirect, url_for
from yrxtx import parse_current, parse_summary
from api_handler import APIHandler
from utils import load_config, save_config

app = Flask(__name__)

# Load configuration
config = load_config()
default_city = config.get("location", "London")
units = config.get("units", "metric")
api_key = config.get("api_key")

# Initialize API handler
api = APIHandler(default_city=default_city, units=units, api_key=api_key)

@app.route('/', methods=['GET'])
def home():
    data = api.fetch_weather()
    weather = parse_current(data)
    return render_template('home.html', weather=weather)

@app.route('/search', methods=['POST'])
def search():
    city = request.form['city']
    api.default_city = city
    data = api.fetch_weather()
    weather = parse_current(data)
    return render_template('home.html', weather=weather)

@app.route('/favorites')
def favorites():
    favs = config.get('favorites', [])
    weather_list = []
    for city in favs:
        api.default_city = city
        data = api.fetch_weather()
        weather_list.append({
            "city": city,
            "weather": parse_current(data)
        })
    return render_template('favorites.html', weather_list=weather_list)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        config['location'] = request.form['default_city']
        config['units'] = request.form['units']
        save_config(config)
        api.default_city = config['location']
        api.units = config['units']
        return redirect(url_for('home'))
    return render_template('settings.html', config=config)

if __name__ == '__main__':
    app.run(debug=True)
# Run the Flask app