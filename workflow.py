from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict, Optional, Any

# === TOOL IMPORTS ===
from utils.weather import print_weather_for_city, get_city_coordinates, get_city_bopunding_box
from utils.attraction_spots import get_attraction_spots
from utils.culinaries import get_topk_restaurants
from utils.transportation import get_flight_results, get_transportation_results, get_nearby_transport
from utils.hotels import get_topk_hotels
from utils.expense_calculation import calculate_expenses
from utils.report_generation import generate_final_report
# === STATE ===
class TravelState(TypedDict):
    user_input: str
    user_input_data: Dict[str, Any]
    destination_details: Dict[str, Any]  # includes latitude, longitude, bounding_box
    weather_info: Optional[Dict]
    hotel_info: Optional[List[Dict]]
    flight_info: Optional[Dict]
    transport_info: Optional[Dict]
    nearby_transport: Optional[List[Dict]]
    restaurant_info: Optional[List[Dict]]
    attraction_info: Optional[List[Dict]]
    expenses: Optional[Dict]
    final_report: Optional[str]

# === AGENT FUNCTIONS ===
def orchestrator(state: TravelState) -> TravelState:
    city = state["user_input_data"]["city"]
    lat, lon = get_city_coordinates(city)
    lon1, lat1, lon2, lat2 = get_city_bopunding_box(lat, lon)
    state["destination_details"] = {
        "latitude": lat,
        "longitude": lon,
        "bounding_box": {"lon1": lon1, "lat1": lat1, "lon2": lon2, "lat2": lat2},
    }
    return state

def weather_agent(state: TravelState) -> TravelState:
    city = state["user_input_data"]["city"]
    result = print_weather_for_city(city)
    state["weather_info"] = result
    return state

def hotel_agent(state: TravelState) -> TravelState:
    city = state["user_input_data"]["city"]
    result = get_topk_hotels(city, topk=5)
    state["hotel_info"] = result
    return state

def flight_agent(state: TravelState) -> TravelState:
    user_input = state["user_input_data"]
    result = get_flight_results(
        origin_city=user_input["origin_city"],
        destination_city=user_input["destination_city"],
        outbound_date=user_input["outbound_date"],
        return_date=user_input["return_date"]
    )
    state["flight_info"] = result
    return state

def transport_agent(state: TravelState) -> TravelState:
    bbx = state["destination_details"]["bounding_box"]
    result = get_transportation_results(
        origin_lat=bbx["lat1"],
        origin_lon=bbx["lon1"],
        dest_lat=bbx["lat2"],
        dest_lon=bbx["lon2"],
        mode="transit"
    )
    state["transport_info"] = result
    return state

def nearby_transport_agent(state: TravelState) -> TravelState:
    lat = state["destination_details"]["latitude"]
    lon = state["destination_details"]["longitude"]
    result = get_nearby_transport(lat=lat, lon=lon, transport_type="metro station")
    state["nearby_transport"] = result
    return state

def restaurant_agent(state: TravelState) -> TravelState:
    city = state["user_input_data"]["city"]
    result = get_topk_restaurants(city, topk=5)
    state["restaurant_info"] = result
    return state

def attraction_agent(state: TravelState) -> TravelState:
    lat = state["destination_details"]["latitude"]
    lon = state["destination_details"]["longitude"]
    result = get_attraction_spots(lat, lon)
    state["attraction_info"] = result
    return state

def expense_agent(state: TravelState) -> TravelState:
    num_days = state["user_input_data"]["num_days"]
    city = state["user_input_data"]["city"]
    currency = "INR"  # Assuming INR for simplicity, can be parameterized
    flight_info = state["flight_info"]
    hotel_info = state["hotel_info"]
    transport_info = state["transport_info"]
    restaurant_info = state["restaurant_info"]
    attraction_info = state["attraction_info"] 

    # Calculate expenses
    expense_report = calculate_expenses(
        city_name=city,
        currency=currency,
        num_days=num_days,
        flight_info=flight_info,
        hotel_info=hotel_info,
        transport_info=transport_info,
        restaurant_info=restaurant_info,
        attraction_info=attraction_info
    )

    state["expenses"] = expense_report
    return state

def fusion_agent(state: TravelState) -> TravelState:
    user_input = state["user_input_data"]
    city = user_input["city"]
    origin_city = user_input["origin_city"]
    destination_city = user_input["destination_city"]
    num_days = user_input["num_days"]
    flight_info = state["flight_info"]
    weather_info = state["weather_info"]
    attraction_info = state["attraction_info"]
    restaurant_info = state["restaurant_info"]
    hotel_info = state["hotel_info"]
    transport_info = state["transport_info"]
    expense_report_text = state["expenses"]
    outbound_date = user_input["outbound_date"]
    return_date = user_input.get("return_date", "")

    # Generate final report
    final_report = generate_final_report(
        origin_city=origin_city,
        destination_city=destination_city,
        num_days=num_days,
        flight_info=flight_info,
        weather_info=weather_info,
        attraction_info=attraction_info,
        restaurant_info=restaurant_info,
        hotel_info=hotel_info,
        transport_info=transport_info,
        expense_report_text=expense_report_text,
        outbound_date=outbound_date,
        return_date=return_date
    )
    state["final_report"] = final_report
    return state

def build_graph():
    """
    Build the state graph for the travel planning workflow.
    This function is used to compile the state graph and can be called directly.
    """
    # === WORKFLOW GRAPH ===
    travel_graph_builder = StateGraph(TravelState)

    travel_graph_builder.set_entry_point("orchestrator")

    travel_graph_builder.add_node("orchestrator", orchestrator)
    travel_graph_builder.add_node("weather", weather_agent)
    travel_graph_builder.add_node("hotel", hotel_agent)
    travel_graph_builder.add_node("flight", flight_agent)
    travel_graph_builder.add_node("transport", transport_agent)
    # travel_graph_builder.add_node("nearby_transport", nearby_transport_agent)
    travel_graph_builder.add_node("restaurant", restaurant_agent)
    travel_graph_builder.add_node("attraction", attraction_agent)
    travel_graph_builder.add_node("expense", expense_agent)
    travel_graph_builder.add_node("fusion", fusion_agent)

    # Add edges
    travel_graph_builder.add_edge("orchestrator", "weather")
    travel_graph_builder.add_edge("weather", "hotel")
    travel_graph_builder.add_edge("hotel", "flight")
    travel_graph_builder.add_edge("flight", "transport")
    travel_graph_builder.add_edge("transport", "restaurant")
    # travel_graph_builder.add_edge("nearby_transport", "restaurant")
    travel_graph_builder.add_edge("restaurant", "attraction")
    travel_graph_builder.add_edge("attraction", "expense")
    travel_graph_builder.add_edge("expense", "fusion")

    travel_graph = travel_graph_builder.compile()
    return travel_graph
