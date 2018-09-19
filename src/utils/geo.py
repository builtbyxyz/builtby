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
    time.sleep(lag)  # wait 1 seconds before each request

    geo_api = 'https://maps.googleapis.com/maps/api/geocode/json'

    with open("utils/secret/googlemaps_apikey.yaml", 'r') as f:
        try:
            credentials = yaml.load(f)
        except yaml.YAMLError as exc:
            print(exc)

    api_key = credentials['API_key']

    geo_params = {
        'address': address,
        'api_key': api_key
    }

    response = requests.get(geo_api, params=geo_params)

    if response.status_code != 200:
        print(f'Request failed, status code {response.status_code}'
              '\nContent:'
              '\n{response.content[:1000]}')
        return None

    else:
        if return_latlon_only:
            results = latlon = response.json()['results']
            if len(results) > 0:
                latlon = results[0]['geometry']['location']
                return latlon['lat'], latlon['lng']
            else:
                print(f"""{response.status_code}: but results were empty""")
                return None, None
        else:
            return response.json()
