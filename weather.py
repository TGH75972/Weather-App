import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def get_weather(city):
    try:
        url = f"https://www.google.com/search?q=weather+{city}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        location = soup.find('div', class_='wob_loc').text
        temperature = soup.find('span', class_='wob_t').text
        weather = soup.find('span', id='wob_dc').text
        humidity = soup.find('span', id='wob_hm').text
        wind = soup.find('span', id='wob_ws').text
        
        return {
            'location': location,
            'temperature': temperature,
            'weather': weather,
            'humidity': humidity,
            'wind': wind
        }
    except Exception as e:
        return {'error': str(e)}

def get_location_by_ip():
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        loc = data['loc'].split(',')
        latitude, longitude = loc[0], loc[1]
        return latitude, longitude
    except Exception as e:
        return None, None

def get_city_name(latitude, longitude):
    try:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse((latitude, longitude), timeout=10)
        return location.address.split(",")[0]
    except GeocoderTimedOut:
        return None

if __name__ == "__main__":
    print("Weather App")
    choice = input("Do you want to use your current location? (yes/no): ").strip().lower()
    
    if choice == 'yes':
        latitude, longitude = get_location_by_ip()
        if latitude and longitude:
            city_name = get_city_name(latitude, longitude)
            if city_name:
                print(f"Detected Location: {city_name}")
                weather_info = get_weather(city_name)
            else:
                print("Could not determine your city name.")
                city = input("Enter the city name: ")
                weather_info = get_weather(city)
        else:
            print("Could not determine your location.")
            city = input("Enter the city name: ")
            weather_info = get_weather(city)
    else:
        city = input("Enter the city name: ")
        weather_info = get_weather(city)
    
    if 'error' in weather_info:
        print(f"Error: {weather_info['error']}")
    else:
        print(f"Location: {weather_info['location']}")
        print(f"Temperature: {weather_info['temperature']}°C")
        print(f"Weather: {weather_info['weather']}")
        print(f"Humidity: {weather_info['humidity']}")
        print(f"Wind: {weather_info['wind']}")
