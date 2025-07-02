import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from langchain_core.tools import tool
from utils.env_config import get_env_variable
# https://api.open-meteo.com/v1/forecast?latitude=17.4065&longitude=78.4772&daily=temperature_2m_max,temperature_2m_min,rain_sum,showers_sum,snowfall_sum&timezone=IST&forecast_days=5
class WeatherService:
    def __init__(self):
        self.geocoding_api_url = "https://geocoding-api.open-meteo.com/v1/search"
        self.weather_api_url = "https://api.open-meteo.com/v1/forecast"
        
    def get_city_coordinates(self, city_name: str) -> Optional[Tuple[float, float]]:
        """
        Convert city name to latitude and longitude coordinates using geocoding API
        """
        try:
            params = {
                "name": city_name,
                "count": 1,
                "language": "en",
                "format": "json"
            }
            
            response = requests.get(self.geocoding_api_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("results") and len(data["results"]) > 0:
                city_data = data["results"][0]
                latitude = city_data["latitude"]
                longitude = city_data["longitude"]
                return latitude, longitude
            else:
                print(f"City '{city_name}' not found")
                return None
                
        except Exception as e:
            print(f"Error fetching coordinates for {city_name}: {e}")
            return None

    def get_bounding_box(self, latitude: float, longitude: float, delta: float = 0.25) -> Tuple[float, float, float, float]:
        """
        Generate a rectangular bounding box around the given coordinates.
        
        Parameters:
            latitude (float): Latitude of the city center
            longitude (float): Longitude of the city center
            delta (float): Half the width/height of the rectangle in degrees (default: 0.1 ~11km)

        Returns:
            Tuple containing (lon1, lat1, lon2, lat2) for use in Geoapify
        """
        lat1 = latitude + delta
        lat2 = latitude - delta
        lon1 = longitude - delta
        lon2 = longitude + delta
        return lon1, lat1, lon2, lat2

    
    def get_weather_forecast(self, latitude: float, longitude: float, days: int = 7) -> Optional[Dict]:
        """
        Get weather forecast for given coordinates
        """
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "daily": "weathercode,temperature_2m_max,temperature_2m_min,rain_sum,showers_sum,snowfall_sum",
                "timezone": "Asia/Kolkata",  # You can use "Asia/Kolkata" for IST explicitly
                "forecast_days": days
            }

            response = requests.get(self.weather_api_url, params=params, timeout=10)
            response.raise_for_status()
            print(response.json())
            return response.json()

        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return None
    
    def get_weather_description(self, weather_code: int) -> str:
        """
        Convert weather code to human-readable description
        """
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }
        return weather_codes.get(weather_code, "Unknown")
    
    def generate_weather_report(self, city_name: str, days: int = 7) -> Dict:
        """
        Generate comprehensive weather report for a city
        """
        coordinates = self.get_city_coordinates(city_name)
        if not coordinates:
            return {"error": f"Could not find coordinates for {city_name}"}
        
        latitude, longitude = coordinates

        weather_data = self.get_weather_forecast(latitude, longitude, days)
        if not weather_data:
            return {"error": f"Could not fetch weather data for {city_name}"}
        
        daily_data = weather_data.get("daily", {})
        
        report = {
            "city": city_name,
            "coordinates": {
                "latitude": latitude,
                "longitude": longitude
            },
            "forecast_days": days,
            "daily_forecast": [],
            "summary": {
                "average_temp": 0,
                "total_precipitation": 0,
                "rainy_days": 0,
                "sunny_days": 0
            }
        }
        
        if daily_data:
            times = daily_data.get("time", [])
            max_temps = daily_data.get("temperature_2m_max", [])
            min_temps = daily_data.get("temperature_2m_min", [])
            precipitations = daily_data.get("precipitation_sum", [])
            weather_codes = daily_data.get("weathercode", [])
            
            total_temp = 0
            
            for i in range(min(len(times), days)):
                date = times[i]
                max_temp = max_temps[i] if i < len(max_temps) else None
                min_temp = min_temps[i] if i < len(min_temps) else None
                precip = precipitations[i] if i < len(precipitations) else None
                weather_code = weather_codes[i] if i < len(weather_codes) else 0
                
                avg_temp = (max_temp + min_temp) / 2 if max_temp is not None and min_temp is not None else None
                total_temp += avg_temp
                
                daily_forecast = {
                    "date": date,
                    "max_temperature": max_temp,
                    "min_temperature": min_temp,
                    "average_temperature": avg_temp,
                    "precipitation": precip,
                    "weather_description": self.get_weather_description(weather_code),
                    "weather_code": weather_code
                }
                
                report["daily_forecast"].append(daily_forecast)

            if len(report["daily_forecast"]) > 0:
                report["summary"]["average_temp"] = total_temp / len(report["daily_forecast"])
        
        return report
    
    def print_weather_report(self, report: Dict) -> None:
        """
        Print formatted weather report
        """
        if "error" in report:
            print(f"Error: {report['error']}")
            return
        
        print(f"\n{'='*60}")
        print(f"WEATHER REPORT FOR {report['city'].upper()}")
        print(f"{'='*60}")
        print(f"Coordinates: {report['coordinates']['latitude']:.4f}, {report['coordinates']['longitude']:.4f}")
        print(f"Forecast Period: {report['forecast_days']} days")
        
        print(f"\nSUMMARY:")
        print(f"  Average Temperature: {report['summary']['average_temp']:.1f}°C")
        
        print(f"\nDAILY FORECAST:")
        print(f"{'Date':<12} {'Max':<6} {'Min':<6} {'Avg':<6}{'Weather':<20}")
        print(f"{'-'*60}")
        
        for day in report["daily_forecast"]:
            date = datetime.fromisoformat(day["date"]).strftime("%Y-%m-%d")
            max_temp = f"{day['max_temperature']:.1f}°C" if day['max_temperature'] is not None else "N/A"
            min_temp = f"{day['min_temperature']:.1f}°C" if day['min_temperature'] is not None else "N/A"
            avg_temp = f"{day['average_temperature']:.1f}°C" if day['average_temperature'] is not None else "N/A"
            weather = day['weather_description'][:18]
            
            print(f"{date:<15} {max_temp:<10} {min_temp:<10} {avg_temp:<10} {weather:<40}")
        
        print(f"{'='*60}\n")

    def get_bounding_box(self, latitude: float, longitude: float, delta: float = 0.25) -> Tuple[float, float, float, float]:
        """
        Generate a rectangular bounding box around the given coordinates.
        
        Parameters:
            latitude (float): Latitude of the city center
            longitude (float): Longitude of the city center
            delta (float): Half the width/height of the rectangle in degrees (default: 0.1 ~11km)

        Returns:
            Tuple containing (lon1, lat1, lon2, lat2) for use in Geoapify
        """
        lat1 = latitude + delta
        lat2 = latitude - delta
        lon1 = longitude - delta
        lon2 = longitude + delta
        return lon1, lat1, lon2, lat2

def get_weather_for_city(city_name: str, days: int = 7) -> Dict:
    """
    Convenience function to get weather report for a city
    """
    weather_service = WeatherService()
    return weather_service.generate_weather_report(city_name, days)

def get_city_coordinates(city_name: str):
    weather_service = WeatherService()
    return weather_service.get_city_coordinates(city_name=city_name)

def get_city_bopunding_box(latitude : str, longitude:str):
     weather_service = WeatherService()
     return weather_service.get_bounding_box(latitude, longitude)

def print_weather_for_city(city_name: str, days: int = 7) -> None:
    """
    Convenience function to print weather report for a city
    """
    weather_service = WeatherService()
    report = weather_service.generate_weather_report(city_name, days)
    weather_service.print_weather_report(report)


