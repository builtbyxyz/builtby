"""Helper functions for BuiltBy API
"""
import requests
import time
import yaml


def get_latlon(address, return_latlon_only=True, lag=2):
    """Use Google Map's Geocoding API to return latitude and longitude when
    given an address

    Arguments:
        address (str)
        return_latlon_only (bool): True (default); returns full output from
            Google API if False

    Returns:
        latitude (float)
        longitude (float)
    """

    geo_api = 'https://maps.googleapis.com/maps/api/geocode/json'

    with open("utils/secret/googlemaps_apikey.yaml", 'r') as f:
        try:
            credentials = yaml.load(f)
        except yaml.YAMLError as exc:
            print(exc)

    api_key = credentials['API_key']

    geo_params = {
        'address': address,
        'key': api_key
    }

    attempts = 0
    results = []

    while len(results) == 0:
        time.sleep(lag)  # wait some time before each request
        response = requests.get(geo_api, params=geo_params)
        results = response.json()['results']

        # if return_latlon_only:

        if len(results) > 0:
            if return_latlon_only:
                latlon = results[0]['geometry']['location']
                return latlon['lat'], latlon['lng']
            else:
                return results
        else:
            attempts += 1
            if attempts == 5:
                print("Reached 5 attempts")
                print(response.json())
                return None, None

    if response.status_code != 200:
        print(f'Request failed, status code {response.status_code}'
              '\nContent:'
              '\n{response.content[:1000]}')
        return None, None
