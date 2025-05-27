from api_handler import fetch_current_weather, fetch_forecast
from utils import load_config, save_config

def main():
    config = load_config()
    
    print("Welcome to the Weather CLI!")
    print("1. Current Weather")
    print("2. 5-Day Forecast")
    print("3. Exit")
    
    while True:
        choice = input("Choose an option (1-3): ")
        
        if choice == '1':
            fetch_current_weather(config)
        elif choice == '2':
            fetch_forecast(config)
        elif choice == '3':
            print("Exiting the Weather CLI. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
