from utils.weather import print_weather_for_city, get_city_coordinates, get_city_bopunding_box
from utils.attraction_spots import get_attraction_spots
from utils.culinaries import get_topk_restaurants
from utils.transportation import get_flight_results, get_transportation_results, get_nearby_transport
from utils.culinaries import get_topk_restaurants
from utils.hotels import get_topk_hotels

def main():
    test_cities = ["Hyderabad"]
    
    for city in test_cities:
        # latitude, longitude = get_city_coordinates(city)
        # lon1, lat1, lon2, lat2 = get_city_bopunding_box(latitude, longitude)
        # response = get_topk_restaurants(lat1, lon1, lat2, lon2)

    #     flights = get_flight_results(
    #     origin_city="HYD", 
    #     destination_city="  PAT", 
    #     outbound_date="2025-07-09", 
    #     return_date="2025-07-10"
    # )
    #     print("Flight Results:", flights)

    #     transport = get_transportation_results(
    #     origin_lat=28.6139, 
    #     origin_lon=77.2090,
    #     dest_lat=28.7041, 
    #     dest_lon=77.1025,
    #     mode="transit"
    # )
    # print("Transportation Results:", transport)

    # nearby = get_nearby_transport(
    #     lat=17.3850, 
    #     lon=78.4867,
    #     transport_type="metro station"
    # )
    # print("Nearby Transport Options:", nearby)

        # restaurants = get_topk_restaurants(city, topk=5)
        # print(f"Top Restaurants in {city}: {restaurants}")

        hotels = get_topk_hotels(city, topk=5)
        print(f"Top Hotels in {city}: {hotels}")
    


if __name__ == "__main__":
    main()
    