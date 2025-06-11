from api_handler import APIHandler
from utils import load_config, save_config

def parse_current(data):
    """Parse current weather data from API response."""
    if not data or 'main' not in data or 'weather' not in data:
        print(" Invalid data received from API.")
        return None
    
    main = data['main']
    weather = data['weather'][0]
    
    return {
        "temperature": main.get('temp'),
        "humidity": main.get('humidity'),
        "description": weather.get('description'),
        "icon": weather.get('icon')
    }

def parse_summary(data):
    """Parse summary weather data from API response."""
    if not data or 'list' not in data:
        print(" Invalid data received from API.")
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
            "icon": weather.get('icon')
        })
    
    return summaries

def print_current_weather(weather):
    if weather is None:
        print("No weather data to display.")
        return
    print("\nCurrent Weather:")
    print(f"Temperature: {weather['temperature']}°")
    print(f"Humidity: {weather['humidity']}%")
    print(f"Description: {weather['description'].capitalize()}")
    print(f"Icon: {weather['icon']}")

def print_forecast(summaries):
    if summaries is None or len(summaries) == 0:
        print("No forecast data to display.")
        return
    print("\nForecast:")
    for summary in summaries[:8]:  # 8 x 3-hour = 1 day, adjust as needed for 3 days
        print(f"{summary['date']}: {summary['temperature']}°, {summary['description'].capitalize()}, Humidity: {summary['humidity']}% (Icon: {summary['icon']})")

def main():
    config = load_config()
    if not config:
        print("❌ Unable to load configuration. Exiting.")
        return
    
    # Initialize APIHandler with loaded config
    api = APIHandler(
        default_city=config.get("location", "London"),
        units=config.get("units", "metric"),
        api_key=config.get("api_key")
    )
    
    while True:
        print("\nWelcome to the Weather CLI!")
        print("1. Current Weather")
        print("2. 3-Day Forecast")
        print("3. Change City")
        print("4. Change Units (°C/°F)")
        print("5. Exit")
        
        choice = input("Choose an option (1-5): ").strip()
        
        if choice == '1':
            data = api.fetch_weather()
            weather = parse_current(data)
            print_current_weather(weather)
        elif choice == '2':
            data = api.fetch_forecast()
            summaries = parse_summary(data)
            print_forecast(summaries)
        elif choice == '3':
            new_city = input("Enter new city: ").strip()
            api.set_city(new_city)
            config['location'] = new_city
            save_config(config)
            print(f"✅ City changed to {new_city}.")
        elif choice == '4':
            new_units = 'imperial' if api.units == 'metric' else 'metric'
            api.set_units(new_units)
            config['units'] = new_units
            save_config(config)
            print(f"✅ Units changed to {new_units}.")
        elif choice == '5':
            print("👋 Exiting the Weather CLI. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
