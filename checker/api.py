#api
import requests
import os
import datetime

api_key = os.environ.get('API_KEY')


class api_request:
    def __init__(self, origin: str, destination:str, dep_date:str) -> None:
        self.origin = origin
        self.destination = destination
        self.dep_date = dep_date
        self.token = api_key
    def cheapest_ticket_in_date(self):

        response_link = f"https://api.travelpayouts.com/aviasales/v3/prices_for_dates?"\
            f"origin={self.origin}"\
            f"&destination={self.destination}"\
            f"&departure_at={self.dep_date}"\
            "&unique=true"\
            "&sorting=price"\
            "&cy=rub"\
            "&limit=5"\
            "&one_way=true"\
            f"&token={self.token}"
        
        response = requests.get(response_link)
        if response.status_code == 200:
            return response 
    def special_offer(self):
        #Специальные предложения 
        response_link = f"https://api.travelpayouts.com/aviasales/v3/get_special_offers?"\
            f"origin={self.origin}&"\
            f"destination={self.destination}&"\
            "locale=ru&"\
            f"token={self.token}"
        
        response = requests.get(response_link)
        if response.status_code == 200:
            return response 
    def two_dest_offer (self):
        response_link = f"http://api.travelpayouts.com/v1/prices/cheap?"\
            f"origin={self.origin}&"\
            f"destination={self.destination}&"\
            f"token={self.token}"
        
        response = requests.get(response_link)
        if response.status_code == 200:
            return response 