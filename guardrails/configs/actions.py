import requests
import os
from typing import Optional


def get_weather_data(context: Dict[str, Any], city_name: Optional[str] = None) -> str:

    # If city_name is not provided or is empty, use a default
    if not city_name:
        return "I need a city name to check the weather."

    # Get API key from environment variables
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "Weather service is currently unavailable."

    try:
        # Make API request
        url = f"https://api.weatherstack.com/current?access_key={api_key}"
        querystring = {"query": city_name}
        response = requests.get(url, params=querystring)
        print(response)
        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            # data = json.loads(response)
            print(data)
            # Extract relevant weather information
            weather_desc = data["current"]["weather_descriptions"][0]
            temperature = data["current"]["temperature"]
            humidity = data["current"]["humidity"]

            return f"{weather_desc.capitalize()} with a temperature of {temperature}°C and {humidity}% humidity."
        else:
            return f"Sorry, I couldn't find weather data for {city_name}."

    except Exception as e:
        print(f"Error fetching weather data: {str(e)}")
        return "I encountered an error while fetching the weather data."
