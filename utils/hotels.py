from typing import List, Dict
import requests
from utils.env_config import get_env_variable

class SerpAPIHotelsFetcher:
    def __init__(self, city_name: str, topk: int = 10):
        self.serpapi_key = get_env_variable("SERPER_API_KEY")
        self.topk = topk
        self.base_url = "https://serpapi.com/search"
        self.city_name = city_name

    def fetch_hotels(self) -> List[Dict]:
        """
        Fetch a list of hotels in the specified city using SerpAPI.
        """
        params = {
            "engine": "google_maps",
            "type": "search",
            "q": f"hotels in area {self.city_name}",
            "api_key": self.serpapi_key,
            "gl": "in",  
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            results = response.json().get("local_results", [])
        except Exception as e:
            print(f"Error fetching hotels in area: {e}")
            return []

        hotels = []
        for h in results[:self.topk]:
            hotel = {
                "name": h.get("title", "Unknown"),
                "address": h.get("address", ""),
                "price_range": h.get("price", "Not available"),
                "type": h.get("type", "Not available"),
                "rating": h.get("rating", None),
                "reviews": h.get("reviews", None),
                "link": h.get("link", "")
            }
            hotels.append(hotel)

        return hotels

def get_topk_hotels(city_name: str, topk: int = 10) -> List[Dict]:
    """
    Get the top K hotels in a specified city.
    
    :param city_name: Name of the city to search for hotels.
    :param topk: Number of top hotels to return.
    :return: List of dictionaries containing hotel information.
    """
    fetcher = SerpAPIHotelsFetcher(city_name, topk)
    return fetcher.fetch_hotels()