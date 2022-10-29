import requests
import os
from typing import Dict


def get_info(url: str, querystring: Dict) -> str:
    """
    Sending the request to API with required parameters
    :param url: request URL, containing the RapidApi Endpoint
    :param querystring: request parameters
    :return: response from API
    """
    headers = {
        "X-RapidAPI-Key": f"{os.getenv('RAPID_API_KEY')}",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    try:
        response = requests.request("GET", url=url, headers=headers, params=querystring)
        if response.status_code == requests.codes.ok:
            return response.text
    except requests.ConnectionError:
        print('Connection failed! Check the URL or request parameters.')
