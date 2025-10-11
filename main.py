import requests
import os
from datetime import datetime
from requests import Response
from twilio.rest import Client
from typing import Union
from dotenv import load_dotenv


def main():
    load_dotenv('.env')

    API_ID: str = os.getenv('HG_BRASIL_API_ID')
    lat: float = os.getenv('LAT')
    long: float = os.getenv('LONG')

    response: Response  = requests.get(f"https://api.hgbrasil.com/weather?key={API_ID}&lat={lat}&lon={long}&user_ip=remote")

    todays_forecast = response.json()['results']['forecast'][0]

    values: dict[str, Union[int, str, float]] = {
        "max_temperature": todays_forecast['max'],
        "min_temperature": todays_forecast['min'],
        "humidity": todays_forecast['humidity'],
        "rain_volume": todays_forecast['rain'],
        "rain_probability": todays_forecast['rain_probability'],
        "description": todays_forecast['description'],
        "wind_speed": todays_forecast['wind_speedy'],
    }


    msg: str = """-\n{description}\nMin:{min_temperature} | Max:{max_temperature}\nProbabilidade de chuva:{rain_probability}\nVento:{wind_speed}\nUmidade:{humidity}""".format(**values)


    ACCOUNT_SID: str = os.getenv('TWILLIO_ACCOUNT_SID')
    AUTH_TOKEN: str = os.getenv('TWILLIO_AUTH_TOKEN')
    sender: int = os.getenv('SENDER')
    receiver: int = os.getenv('RECEIVER')


    client: Client = Client(ACCOUNT_SID, AUTH_TOKEN)
    client.messages.create(
        body=msg,
        from_=sender,
        to=receiver
    )

if __name__ == "__main__":
    main()
