import requests
from utils import load_config

def fetch_current_weather(config):
    api_key = config['api_key']
    location = config['location']
    units = config['units']
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units={units}"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            print(f"🌤️ {data['name']}, {data['sys']['country']} | {data['main']['temp']}° | Humidity: {data['main']['humidity']}% | {data['weather'][0]['description'].capitalize()}")
        else:
            print(f"Error: {data.get('message', 'Unable to fetch data')}")
    except Exception as e:
        print(f"Exception: {e}")

def fetch_forecast(config):
    api_key = config['api_key']
    location = config['location']
    units = config['units']
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units={units}"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            print("📅 5-Day Forecast:")
            for i in range(0, len(data['list']), 8):
                entry = data['list'][i]
                date = entry['dt_txt'].split(" ")[0]
                temp = entry['main']['temp']
                desc = entry['weather'][0]['description'].capitalize()
                print(f"{date}: {temp}° | {desc}")
        else:
            print(f"Error: {data.get('message', 'Unable to fetch forecast')}")
    except Exception as e:
        print(f"Exception: {e}")
