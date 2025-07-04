import os
import requests
from typing import List, Dict, Optional, Tuple
from dotenv import load_dotenv
from utils.env_config  import get_env_variable

load_dotenv()

class GeoapifyAttractionSpotGenerator:
    def __init__(self, latitude: float, longitude: float, radius: int = 5000, categories: Optional[str] = None, limit: int = 10, lang: str = 'en'):
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
        self.categories = categories or "tourism,tourism.sights,tourism.attraction,entertainment.museum,leisure.park"
        self.limit = limit
        self.lang = lang
        self.api_key = get_env_variable("GEOAPIFY_API_KEY")
        if not self.api_key:
            raise ValueError("GEOAPIFY_API_KEY not found in environment variables.")
        self.base_url = "https://api.geoapify.com/v2/places"

    def fetch_attraction_spots(self) -> List[Dict]:
        try:
            lon1, lat1, lon2, lat2 = self.get_bounding_box(self.latitude, self.longitude)
        except Exception as e:
            print(f"Error generating bounding box: {e}")
            return []

        params = {
            "filter": f"rect:{lon1},{lat1},{lon2},{lat2}",
            "categories": self.categories,  # e.g., "tourism,tourism.sights,entertainment.museum,leisure.park"
            "limit": self.limit,
            "apiKey": self.api_key
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"Error fetching attraction spots: {e}")
            return []

        spots = []
        for feature in data.get('features', []):
            prop = feature.get('properties', {})
            coordinates = feature.get('geometry', {}).get('coordinates', [None, None])

            spot = {
                "name": prop.get('name') or 'Unknown',
                "address": f"{prop.get('address_line1', '')}, {prop.get('address_line2', '')}".strip(', '),
                "categories": prop.get('categories', []),
                "opening_hours": prop.get('opening_hours', 'Not available'),
                "website": prop.get('website', ''),
                "contacts": prop.get('contact'),
                "lat": coordinates[1] if len(coordinates) > 1 else None,
                "lon": coordinates[0] if len(coordinates) > 0 else None,
                "place_id": prop.get('place_id', ''),
            }
            spots.append(spot)

        return spots
    

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

# Example utility function

def get_attraction_spots(latitude: float, longitude: float, radius: int = 5000, limit: int = 10) -> List[Dict]:
    """
    Get a list of attraction spots for a given location using Geoapify.
    """
    generator = GeoapifyAttractionSpotGenerator(latitude, longitude, radius=radius, limit=limit)
    return generator.fetch_attraction_spots()
