from typing import List, Dict, Optional, Any
import requests
from utils.env_config import get_env_variable
import logging
import aiohttp

logger = logging.getLogger(__name__)

SERP_API_KEY = get_env_variable("SERPER_API_KEY")

class FlightRequest:
    def __init__(self, origin: str, destination: str, outbound_date: str, return_date: Optional[str] = None):
        self.origin = origin
        self.destination = destination
        self.outbound_date = outbound_date
        self.return_date = return_date

class TransportationService:
    def __init__(self):
        self.serpapi_key = SERP_API_KEY
        self.base_url = "https://serpapi.com/search.json"

    def search_flights(self, origin_city: str, destination_city: str,
                       outbound_date: str, return_date: Optional[str] = None) -> List[Dict]:
        """
        Search for flights using SerpAPI Google Flights engine.
        """
        logger.info(f"Searching flights: {origin_city} to {destination_city}")

        params = {
            "api_key": self.serpapi_key,
            "engine": "google_flights",
            "hl": "en",
            "gl": "in",  # ✅ as per working URL
            "departure_id": origin_city.strip().upper(),
            "arrival_id": destination_city.strip().upper(),
            "outbound_date": outbound_date,
            "return_date": return_date if return_date else "",
            "currency": "INR"
        }

        if return_date:
            params["return_date"] = return_date

        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            search_results = response.json()
            logger.debug(f"Search results: {search_results}")

            best_flights = search_results.get("best_flights", [])
            other_flights = search_results.get("other_flights", [])

            all_flights = best_flights + other_flights
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP error while fetching flights: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

        return all_flights

    def get_local_transportation(self, origin_lat: float, origin_lon: float,
                                  dest_lat: float, dest_lon: float,
                                  mode: str = "transit") -> Dict[str, Any]:
        """
        Get local transportation options using SerpAPI Google Maps engine.
        """
        logger.info(f"Searching local transportation via {mode}")

        # Midpoint for the search area
        center_lat = (origin_lat + dest_lat) / 2
        center_lon = (origin_lon + dest_lon) / 2
        zoom = 14

        # Construct query string to mimic a user search
        query = f"local transport from {origin_lat},{origin_lon} to {dest_lat},{dest_lon} by {mode}"

        params = {
            "api_key": self.serpapi_key,
            "engine": "google_maps",
            "type": "search",
            "q": query,
            "ll": f"@{center_lat},{center_lon},{zoom}z",
            "hl": "en"
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=15)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching local transportation: {e}")
            return {}

    def get_nearby_transport_options(self, lat: float, lon: float, transport_type: str = "public_transport") -> List[Dict]:
        """
        Get nearby transportation options (bus stops, metro stations, etc.) using SerpAPI.
        """
        logger.info(f"Searching nearby {transport_type} options")
        
        params = {
            "api_key": self.serpapi_key,
            "engine": "google_maps",
            "type": "search",
            "q": transport_type,
            "ll": f"@{lat},{lon},14z"
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=15)
            response.raise_for_status()
            results = response.json().get("local_results", [])
            return results
        except Exception as e:
            logger.error(f"Error fetching nearby transport options: {e}")
            return []

# Utility functions for easy access

def get_flight_results(origin_city: str, destination_city: str, outbound_date: str, return_date: Optional[str] = None) -> List[Dict]:
    """
    Get flight search results with coordinates and city names.
    """
    service = TransportationService()
    return service.search_flights(origin_city, destination_city, outbound_date, return_date)

def get_transportation_results(origin_lat: float, origin_lon: float, dest_lat: float, dest_lon: float, 
                             mode: str = "transit") -> Dict[str, Any]:
    """
    Get local transportation results between two points.
    """
    service = TransportationService()
    return service.get_local_transportation(origin_lat, origin_lon, dest_lat, dest_lon, mode)

def get_nearby_transport(lat: float, lon: float, transport_type: str = "public_transport") -> List[Dict]:
    """
    Get nearby transportation options.
    """
    service = TransportationService()
    return service.get_nearby_transport_options(lat, lon, transport_type)

# Example usage functions
def example_flight_search():
    """
    Example of how to use flight search.
    """
    flights = get_flight_results(
        origin_city="DEL", 
        destination_city="BOM", 
        origin_lat=28.6139, 
        origin_lon=77.2090,
        dest_lat=19.0760, 
        dest_lon=72.8777,
        outbound_date="2024-07-01", 
        return_date="2024-07-10"
    )
    print("Flight Results:", flights)

def example_transportation_search():
    """
    Example of how to use transportation search.
    """
    transport = get_transportation_results(
        origin_lat=28.6139, 
        origin_lon=77.2090,
        dest_lat=28.7041, 
        dest_lon=77.1025,
        mode="transit"
    )
    print("Transportation Results:", transport)

def example_nearby_transport():
    """
    Example of how to use nearby transport search.
    """
    nearby = get_nearby_transport(
        lat=28.6139, 
        lon=77.2090,
        transport_type="metro station"
    )
    print("Nearby Transport Options:", nearby)
