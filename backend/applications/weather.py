import os
from dotenv import load_dotenv
import requests

load_dotenv("../.env")  # load variables from .env file

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city_name):
    params = {"q": city_name, "appid": API_KEY, "units": "metric"}
    resp = requests.get(BASE_URL, params=params)
    data = resp.json()
    if resp.status_code != 200:
        print(f"Error: {data.get('message')}")
        return
    weather = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    print(f"Weather in {city_name}: {weather}, {temp}°C")

if __name__ == "__main__":
    city = input("Enter city name: ")
    get_weather(city)
