import requests
import os


def get_info(url, querystring):
    headers = {
        "X-RapidAPI-Key": f"{os.getenv('RAPID_API_KEY')}",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    try:
        response = requests.request("GET", url=url, headers=headers, params=querystring, timeout=10)
        if response.status_code == requests.codes.ok:
            return response.text
    except requests.ConnectionError:
        print('Connection failed! Check the URL or request parameters.')

# url = 'https://hotels4.p.rapidapi.com/locations/v2/search'
# querystring = {"query": f"{place}", "locale": "en_US", "currency": "USD"}


