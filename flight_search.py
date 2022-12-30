import requests
import os
from flight_data import FlightData
from pprint import pprint


TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = os.environ["ENV_TEQUILA_API_KEY"]


class FlightSearch:

    def __init__(self):
        self.headers = {
            "apikey": TEQUILA_API_KEY
        }

    # This class is responsible for talking to the Flight Search API.
    def get_destination_code(self, city_name):
        parameters = {
            "location_types": "city",
            "term": city_name,
            "limit": 1
        }
        response = requests.get(url=f"{TEQUILA_ENDPOINT}/locations/query",
                                headers=self.headers,
                                params=parameters)
        data = response.json()["locations"][0]
        code = data["code"]
        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time, max_stopovers=0):
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": max_stopovers,
            "curr": "GBP"
        }
        response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search",
                                headers=self.headers,
                                params=query)
        try:
            data = response.json()["data"][0]
        except IndexError:
            query["max_stopovers"] = 1
            response = requests.get(
                url=f"{TEQUILA_ENDPOINT}/v2/search",
                headers=self.headers,
                params=query,
            )
            data = response.json()["data"][0]
            pprint(data)

            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][1]["cityTo"],
                destination_airport=data["route"][1]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][2]["local_departure"].split("T")[0],
                stop_overs=1,
                via_city=data["route"][0]["cityTo"]
            )
            return flight_data
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )

            print(f"{flight_data.destination_city}: £{flight_data.price}")
            return flight_data
