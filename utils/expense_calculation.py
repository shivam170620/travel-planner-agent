from typing import Dict, Any, List
from utils.llm_wrapper.llms import llm
from utils.config import EXPENSE_MANAGEMENT_PROMPT
from langchain_core.prompts import PromptTemplate

class ExpenseReportGenerator:
    def __init__(
        self,
        city_name: str,
        currency: str,
        num_days: int,
        flight_info: Dict[str, Any],
        hotel_info: list,
        transport_info: Dict[str, Any],
        restaurant_info: list,
        attraction_info: list
    ):
        self.city_name = city_name
        self.currency = currency
        self.num_days = num_days
        self.flight_info = flight_info
        self.hotel_info = hotel_info
        self.transport_info = transport_info
        self.restaurant_info = restaurant_info
        self.attraction_info = attraction_info
        self.expense_report = ""
    
    def generate_report(self) -> str:        
        """
        Generate a detailed expense report for the trip.
        """
        prompt = PromptTemplate.from_template(
            EXPENSE_MANAGEMENT_PROMPT
        )
        formatted_prompt = prompt.format(
            city_name=self.city_name,
            currency=self.currency,
            num_days=self.num_days,
            flight_info=self.flight_info,
            hotel_info=self.hotel_info,
            transport_info=self.transport_info,
            restaurant_info=self.restaurant_info,
            attraction_info=self.attraction_info
        )

        response = llm.invoke(formatted_prompt)
        if response and isinstance(response, str):
            self.expense_report = response.content
        else:
            self.expense_report = "Failed to generate report. Please check the input data or try again later."

        return self.expense_report

def calculate_expenses(
    city_name: str,
    currency: str,
    num_days: int,
    flight_info: Dict[str, Any],
    hotel_info: List[Dict[str, Any]],
    transport_info: Dict[str, Any],
    restaurant_info: List[Dict[str, Any]],
    attraction_info: List[Dict[str, Any]]
) -> str:
    """
    Calculate and generate a detailed expense report for the trip.
    
    :param city_name: Name of the city for the trip.
    :param currency: Currency for the expenses.
    :param num_days: Number of days for the trip.
    :param flight_info: Information about flights.
    :param hotel_info: List of hotels with nightly rates.
    :param transport_info: Average transportation cost.
    :param restaurant_info: List of top restaurants with meal costs.
    :param attraction_info: List of attractions with ticket prices.
    
    :return: A formatted expense report as a string.
    """
    generator = ExpenseReportGenerator(
        city_name=city_name,
        currency=currency,
        num_days=num_days,
        flight_info=flight_info,
        hotel_info=hotel_info,
        transport_info=transport_info,
        restaurant_info=restaurant_info,
        attraction_info=attraction_info
    )
    
    return generator.generate_report()

