"""Helper functions for BuiltBy API
"""
import requests
import time


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

    geo_params = {
        'address': address
    }

    response = requests.get(geo_api, params=geo_params)

    if response.status_code == 200:
        if return_latlon_only:
            results = latlon = response.json()['results']
            if len(results) > 0:
                latlon = results[0]['geometry']['location']
                return latlon['lat'], latlon['lng']
            else:
                print(f"{response.status_code}: But index error?")
                return None, None
        else:
            return response.json()
    else:
        print(f"{response.status_code}: Could not return lat and lon results.")
        return None
