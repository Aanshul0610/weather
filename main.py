import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel('Enter City:', self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton('Get Weather', self)
        self.temperature_label = QLabel('', self)
        self.emoji_label = QLabel('', self)
        self.description_label = QLabel('', self)
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Weather App')
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        self.setLayout(vbox)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.city_label.setObjectName('city_label')
        self.city_input.setObjectName('city_input')
        self.get_weather_button.setObjectName('get_weather_button')
        self.temperature_label.setObjectName('temperature_label')
        self.emoji_label.setObjectName('emoji_label')
        self.description_label.setObjectName('description_label')
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial, sans-serif;
            }
            QLabel {
                font-size: 18px;
                color: #333;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                padding: 10px;
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.get_weather_button.clicked.connect(self.get_weather)
    
    def get_weather(self):
        api_key = "0dcd828339eb3ae37af13ff25f0eb362"
        city= self.city_input.text()
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()

            if response.status_code == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request:\n Please check the city name.")
                case 401:
                    self.display_error("Unauthorized:\n Please check your API key.")
                case 403:
                    self.display_error("Forbidden:\n You do not have permission to access this resource.")
                case 404:
                    self.display_error("City not found:\n Please check the city name.")
                case 500:
                    self.display_error("Internal Server Error:\n Please try again later.")
                case 503:
                    self.display_error("Service Unavailable:\n Please try again later.")
                case 504:
                    self.display_error("Gateway Timeout\n Please try again later.")
                case _:
                    self.display_error(f"An unexpected error occurred: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("Connection Error\n Please check your internet connection.")
        except requests.exceptions.Timeout:
            print("Timeout Error\n The request timed out.")
        except requests.exceptions.TooManyRedirects:
            print("Too Many Redirects\n Please check the URL.")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
    def display_error(self,message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px;")

        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]


        self.temperature_label.setText(f"{temperature_c:.1f}°C")  # Celsius shown in UI now
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description.capitalize())

    @staticmethod
    def get_weather_emoji(weather_id):
        if weather_id >= 200 and weather_id < 232:
            return "⛈️"
        elif weather_id >= 300 and weather_id < 321:
            return "🌧️"
        elif weather_id >= 500 and weather_id < 532:
            return "🌧️"
        elif weather_id >= 600 and weather_id < 622:
            return "❄️"
        elif weather_id >= 701 and weather_id < 781:
            return "🌫️"
        elif weather_id == 800:
            return "☀️"
        elif weather_id >= 801 and weather_id < 804:
            return "🌤️"
        elif weather_id >= 804:
            return "☁️"
        else:
            return "❓"



        

if __name__ == '__main__':
        app= QApplication(sys.argv)
        weather_app = WeatherApp()
        weather_app.show()
        sys.exit(app.exec_())


 