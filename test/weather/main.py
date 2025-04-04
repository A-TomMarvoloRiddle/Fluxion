import requests
import vc
import RNN_hardcoding

def handle_extreme_weather(condition):
    if "fog" or "storm" in condition.lower():
        RNN_hardcoding.predict()
    else:
        green_light_times = vc.start_system()
        print("Green Light Times:", green_light_times)

def fetch_weather(api_key, city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        weather_condition = weather_data['weather'][0]['description']
        print(f"Current weather in {city}: {weather_condition.capitalize()}")
        handle_extreme_weather(weather_condition)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")

# Replace with your OpenWeatherMap API key and desired city
api_key = "b76f2a6e991b546ee2826c5776305ed8"
city = "Mumbai"

fetch_weather(api_key, city)
