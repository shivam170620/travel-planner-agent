import requests
from typing import List, Dict, Optional
import os
from utils.env_config import get_env_variable

class SerpApiRestaurantFetcher:
    def __init__(self, city_name : str,topk: int = 10):
    
        self.serpapi_key = get_env_variable("SERPER_API_KEY")
        self.topk = topk
        self.base_url = "https://serpapi.com/search"
        self.city_name = city_name

    def fetch_restaurants(self) -> List[Dict]:
        # Calculate center point and zoom leve
        
        params = {
            "engine": "google_maps",
            "type": "search",
            "q": f"restaurants in area {self.city_name}",
            "api_key": self.serpapi_key
        }
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            results = response.json().get("local_results", [])
        except Exception as e:
            print(f"Error fetching restaurants in area: {e}")
            return []

        restaurants = []
        for r in results[:self.topk]:
            restaurant = {
                "name": r.get("title", "Unknown"),
                "address": r.get("address", ""),
                "avg_meal_price": r.get("price", "Not available"),
                "meals_available": r.get("type", "Not available"),
                "rating": r.get("rating", None),
                "reviews": r.get("reviews", None),
                "link": r.get("link", "")
            }
            restaurants.append(restaurant)
        return restaurants

def get_topk_restaurants(city_name: str, topk: int = 10) -> List[Dict]:
    fetcher = SerpApiRestaurantFetcher(city_name, topk)
    return fetcher.fetch_restaurants() 