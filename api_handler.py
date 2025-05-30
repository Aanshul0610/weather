import requests

class APIHandler:
    def __init__(self, default_city="London", units="metric", api_key=None):
        self.base_url = "https://api.weatherapi.com/v1/current.json"
        self.units = units
        self.api_key = api_key or 'dbf62e8a2cb24229a1f150051252905'
        self.default_city = default_city
        self.aqi = "yes"

    def fetch_weather(self):
        """
        Fetch and display current weather data from WeatherAPI.
        """
        params = {
            'key': self.api_key,
            'q': self.default_city,
            'aqi': self.aqi
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            print(f"Current weather in {data['location']['name']}, {data['location']['country']}:")
            print(f"Temperature: {data['current']['temp_c']}°C")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
    def fetch_forecast(self):
        """
        Fetch and display 5-day weather forecast from WeatherAPI.
        """
        # Placeholder for forecast functionality
        print("🔔 Forecast feature not implemented yet.")
    def set_city(self, city):
        """        Set the city for which weather data will be fetched.
        """
        self.default_city = city
        print(f"City set to {self.default_city}.")
    def set_units(self, units):
        """        Set the units for temperature (metric or imperial).
        """
        self.units = units
        print(f"Units set to {self.units}.")
    def set_aqi(self, aqi):
        """        Set the Air Quality Index (AQI) preference.
        """
        self.aqi = aqi
        print(f"AQI preference set to {self.aqi}.")
    def get_current_city(self):
        """        Get the current city for which weather data is fetched.
        """
        return self.default_city
    def get_units(self):
        """        Get the current units for temperature.
        """
        return self.units
    def get_aqi(self):
        """        Get the current AQI preference.
        """
        return self.aqi
    def get_api_key(self):
        """        Get the current API key.
        """
        return self.api_key
    def set_api_key(self, api_key):
        """        Set a new API key.
        """
        self.api_key = api_key
        print(f"API key set to {self.api_key}.")
    def get_base_url(self):
        """        Get the base URL for the API.
        """
        return self.base_url
            
        