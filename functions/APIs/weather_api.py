import os, requests, json
from dotenv import load_dotenv
from google.genai import types

def get_weather(query):
    try:
        load_dotenv();
        api_key = os.environ.get("WEATHER_API_KEY")

    except Exception as e:
        print(f"Error: {e}");
        return

    if not api_key:
        return {
            "success": False,
            "error": "Weather API key not found."
        }

    url = "http://api.weatherstack.com/current"

    params = {
        "access_key": api_key,
        "query": query
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()

        data = response.json()

        if "error" in data and data.get("error"):
            error_info = data.get("error", {})
            return {
                "success": False,
                "error": {
                    "code": error_info.get("code"),
                    "type": error_info.get("type"),
                    "info": error_info.get("info")
                }
            }

        current = data.get("current", {})
        location = data.get("location", {})

        return {
            "success": True,
            "location": {
                "name": location.get("name"),
                "country": location.get("country"),
                "region": location.get("region"),
                "lat": location.get("lat"),
                "lon": location.get("lon"),
                "timezone_id": location.get("timezone_id"),
                "localtime": location.get("localtime"),
            },
            "weather": {
                "temperature": current.get("temperature"),
                "feelslike": current.get("feelslike"),
                "weather_description": current.get("weather_description", []),
                "weather_code": current.get("weather_code"),
                "wind_speed": current.get("wind_speed"),
                "wind_degree": current.get("wind_degree"),
                "wind_dir": current.get("wind_dir"),
                "pressure": current.get("pressure"),
                "precip": current.get("precip"),
                "humidity": current.get("humidity"),
                "cloudcover": current.get("cloudcover"),
                "visibility": current.get("visibility"),
                "uv_index": current.get("uv_index"),
                "is_day": current.get("is_day") == "yes"
            },
            "observation_time": current.get("observation_time"),
            "units": data.get("request", {}).get("unit")
        }
    
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Connection error"}
    except requests.exceptions.HTTPError as e:
        return {"success": False, "error": f"HTTP error: {str(e)}"}
    except Exception as e:
        return {"sucess": False, "error": f'Error: {str(e)}'}


schema_get_weather = types.FunctionDeclaration(
    name="get_weather", 
    description="Get the current weather information from a location.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "query": {
                "type": "string",
                "description": "City name, Zip code, or latitude, longitude (e.g., 'New York', '10001', '40.7128,-74.0060')"
            }
        },
        required=["query"], 
    ),
)