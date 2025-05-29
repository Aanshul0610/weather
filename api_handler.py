import requests

class APIHandler:
    def __init__(self, default_city="London", units="metric", api_key=None):
        self.base_url = "https://api.weatherapi.com/v1/current.json"
        self.units = units
        self.api_key = api_key or '36819401e39b47cfb7382236252805'
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

        