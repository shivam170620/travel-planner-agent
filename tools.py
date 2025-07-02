from langchain_core.tools import tool
from utils.weather import get_weather_for_city
from utils.attraction_spots import get_attraction_spots

@tool
def get_weather_for_city(city_name: str, days: int = 7) -> str:
    """
    Args:
        city_name: The name of the city to get the weather forecast for.
        days: The number of days to get the weather forecast for.
    Returns:
        The weather report for the given city for the next d days.
        Get the weather forecast for a given city.
        It generates the weather report for the given city for the next d days.

        Example:
        WEATHER REPORT FOR KASHMIR
        ============================================================
        Coordinates: 25.6958, 58.8789
        Forecast Period: 5 days

        SUMMARY:
        Average Temperature: 34.6°C

        DAILY FORECAST:
        Date         Max    Min    Avg    Precip   Weather             
        ------------------------------------------------------------
        2025-06-29      38.6°C     30.7°C     34.6°C     Overcast                                
        2025-06-30      39.5°C     30.2°C     34.9°C     Mainly clear                            
        2025-07-01      40.1°C     30.6°C     35.4°C     Mainly clear                            
        2025-07-02      38.8°C     29.7°C     34.2°C     Partly cloudy                           
        2025-07-03      38.4°C     29.8°C     34.1°C     Partly cloudy 
    """
    return get_weather_for_city(city_name, days)

@tool
def get_attraction_spots(city_name: str) -> str:
    """
    Args:
        city_name: The name of the city to get the attraction spots for.
    Returns:
        The attraction spots for the given city.
    """
    return get_attraction_spots(city_name)