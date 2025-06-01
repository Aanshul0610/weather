from api_handler import APIHandler
from utils import load_config, save_config

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
        print("2. 5-Day Forecast")
        print("3. Change City")
        print("4. Change Units (°C/°F)")
        print("5. Exit")
        
        choice = input("Choose an option (1-5): ").strip()
        
        if choice == '1':
            api.fetch_weather()
        elif choice == '2':
            print("🔔 Forecast feature not implemented yet.")  # Placeholder
        elif choice == '3':
            new_city = input("Enter new city: ").strip()
            api.set_city(new_city)
            config['location'] = new_city
            save_config(config)
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
# This script is a command-line interface (CLI) for a weather application.
# It allows users to fetch current weather data, view a 5-day forecast (not implemented),
# change the city for which weather data is fetched, and toggle between metric and imperial units.
# The configuration is loaded from a JSON file, and any changes made by the user are saved back to this file