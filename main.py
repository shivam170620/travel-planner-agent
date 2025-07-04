from workflow import build_graph

def main():
    input_state = {
        "user_input": "Plan a 2-day trip to Hyderabad",
        "user_input_data": {
            "city": "Hyderabad",
            "origin_city": "PAT",
            "destination_city": "HYD",
            "outbound_date": "2025-07-09",
            "return_date": "2025-07-10",
            "num_days": 2
        },
        "destination_details": {}
    }
    travel_graph = build_graph()
    result = travel_graph.invoke(input_state)
    print(result["final_report"])

if __name__ == "__main__":
    main()
    