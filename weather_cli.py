from datetime import datetime
from api_handler import APIHandler
from utils import load_config, save_config

def parse_current(data):
    if not data or 'main' not in data or 'weather' not in data:
        return {}

    # Convert timestamps to readable time
    sunrise = datetime.utcfromtimestamp(data.get('sys', {}).get('sunrise', 0)).strftime('%H:%M:%S') if data.get('sys', {}).get('sunrise') else "-"
    sunset = datetime.utcfromtimestamp(data.get('sys', {}).get('sunset', 0)).strftime('%H:%M:%S') if data.get('sys', {}).get('sunset') else "-"
    
    return {
        "city": data.get("name", "-"),
        "temperature": data["main"].get("temp", "-"),
        "feels_like": data["main"].get("feels_like", "-"),
        "temp_min": data["main"].get("temp_min", "-"),
        "temp_max": data["main"].get("temp_max", "-"),
        "humidity": data["main"].get("humidity", "-"),
        "wind_speed": data.get("wind", {}).get("speed", "-"),
        "wind_deg": data.get("wind", {}).get("deg", "-"),
        "pressure": data["main"].get("pressure", "-"),
        "description": data["weather"][0].get("description", "-"),
        "sunrise": sunrise,
        "sunset": sunset,
    }

def parse_summary(data):
    """Parse summary weather data from API response."""
    if not data or 'list' not in data:
        print("Invalid data received from API.")
        return None
    
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

def print_current_weather(weather, units):
    if not weather:
        print("No weather data to display.")
        return
    
    unit_symbol = '°C' if units == 'metric' else '°F'
    wind_unit = 'm/s' if units == 'metric' else 'mph'
    
    print("\nCurrent Weather:")
    print(f"Location: {weather['city']}")
    print(f"Conditions: {weather['description'].capitalize()}")
    print(f"Temperature: {weather['temperature']}{unit_symbol} (Feels like: {weather['feels_like']}{unit_symbol})")
    print(f"Min/Max: {weather['temp_min']}{unit_symbol} | {weather['temp_max']}{unit_symbol}")
    print(f"Humidity: {weather['humidity']}%")
    print(f"Wind: {weather['wind_speed']} {wind_unit} at {weather['wind_deg']}°")
    print(f"Pressure: {weather['pressure']} hPa")
    print(f"Sunrise: {weather['sunrise']} UTC | Sunset: {weather['sunset']} UTC")

def format_forecast_date(dt_str):
    try:
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%a %m/%d %H:%M")
    except (ValueError, TypeError):
        return dt_str

def print_forecast(summaries, units):
    if not summaries:
        print("No forecast data to display.")
        return
    
    unit_symbol = '°C' if units == 'metric' else '°F'
    wind_unit = 'm/s' if units == 'metric' else 'mph'
    
    print("\n3-Day Forecast:")
    print("{:<20} {:<8} {:<15} {:<10} {:<10}".format(
        "Date/Time", "Temp", "Conditions", "Humidity", "Wind"
    ))
    print("-" * 65)
    
    for summary in summaries[:24]:  # 24 intervals = 3 days (8 per day)
        formatted_date = format_forecast_date(summary['date'])
        print("{:<20} {:<8} {:<15} {:<10} {:<10}".format(
            formatted_date,
            f"{summary['temperature']}{unit_symbol}",
            summary['description'].capitalize(),
            f"{summary['humidity']}%",
            f"{summary['wind_speed']} {wind_unit}"
        ))

def main():
    config = load_config()
    if not config:
        print("Unable to load configuration. Exiting.")
        return
    
    # Initialize APIHandler with loaded config
    api = APIHandler(
        default_city=config.get("location", "London"),
        units=config.get("units", "metric"),
        api_key=config.get("api_key")
    )
    
    while True:
        print("\n🌦️ Weather CLI 🌤️")
        print("1. Current Weather")
        print("2. 3-Day Forecast")
        print("3. Change City")
        print("4. Change Units (°C/°F)")
        print("5. Exit")
        
        choice = input("Choose an option (1-5): ").strip()
        
        if choice == '1':
            data = api.fetch_weather()
            weather = parse_current(data)
            print_current_weather(weather, api.units)
        elif choice == '2':
            data = api.fetch_forecast()
            summaries = parse_summary(data)
            print_forecast(summaries, api.units)
        elif choice == '3':
            new_city = input("Enter new city: ").strip()
            if new_city:
                api.set_city(new_city)
                config['location'] = new_city
                save_config(config)
                print(f"✅ City changed to {new_city}.")
            else:
                print("⚠️ City name cannot be empty.")
        elif choice == '4':
            current_units = api.units
            new_units = 'imperial' if current_units == 'metric' else 'metric'
            api.set_units(new_units)
            config['units'] = new_units
            save_config(config)
            unit_name = 'Fahrenheit (°F)' if new_units == 'imperial' else 'Celsius (°C)'
            print(f"✅ Units changed to {unit_name}.")
        elif choice == '5':
            print("👋 Exiting the Weather CLI. Goodbye!")
            break
        else:
            print("⚠️ Invalid choice. Please enter a number between 1-5.")

if __name__ == "__main__":
    main()