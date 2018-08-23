"""API for retrieving permit data

Example of GET request

    # In the terminal
    $ curl http://localhost:5000/new

    OR

    # Python
    requests.get('http://localhost:5000/new').json()

"""

from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from pymongo import MongoClient
import json
import requests
from utils.manage_params import manage_params

app = Flask(__name__)
api = Api(app)
CORS(app)
auth = HTTPBasicAuth()


parser = reqparse.RequestParser()
with open('supported_args.txt', 'r') as f:
    supp_args = f.readlines()
    for arg in supp_args:
        parser.add_argument(arg.rstrip('\n'))


# USER_DATA = {
#     'admin': 'builtby2018'
# }


with open('../data/new_projects.json', 'r') as f:
    NEW_PROJECTS = json.load(f)

mc = MongoClient('localhost', 27017)
db = mc['builtby']
COMPANIES = list(db['companies_20180816'].find())

# convert mongo objectid object to string for json serialization
for company in COMPANIES:
    company['_id'] = str(company['_id'])


# @auth.verify_password
# def verify(username, password):
#     if not (username and password):
#         return False
#     return USER_DATA.get(username) == password


# ----- RESOURCES -----
# shows a list of all permits
class Permit_LandUse(Resource):
    # @auth.login_required
    def get(self):
        """Return all permit applications from the Seattle Open Data
        """
        url = 'https://data.seattle.gov/resource/meme-txgf'
        # get arguments passed by user
        args = parser.parse_args()
        # compile params dict with args
        params = manage_params(args)
        response = requests.get(url, params=params)
        LANDUSE = response.json()
        return LANDUSE


class Permit_Building(Resource):
    # @auth.login_required
    def get(self):
        """Return all permit applications from the Seattle Open Data
        """
        url = 'https://data.seattle.gov/resource/k44w-2dcq'
        # get arguments passed by user
        args = parser.parse_args()
        # compile params dict with args
        params = manage_params(args)
        response = requests.get(url, params=params)
        BUILDINGS = response.json()
        return BUILDINGS


class Permit_Electrical(Resource):
    # @auth.login_required
    def get(self):
        """Return all permit applications from the Seattle Open Data
        """
        url = 'https://data.seattle.gov/resource/axxs-4epa'
        # get arguments passed by user
        args = parser.parse_args()
        # compile params dict with args
        params = manage_params(args)
        response = requests.get(url, params=params)
        ELECTRICAL = response.json()
        return ELECTRICAL


class Permit_Trade(Resource):
    # @auth.login_required
    def get(self):
        """Return all permit applications from the Seattle Open Data
        """
        url = 'https://data.seattle.gov/resource/rqjp-prb2'
        # get arguments passed by user
        args = parser.parse_args()
        # compile params dict with args
        params = manage_params(args)
        response = requests.get(url, params=params)
        TRADE = response.json()
        return TRADE


# shows projects with upcoming design review meetings
class NewProjectsList(Resource):
    # @auth.login_required
    def get(self):
        """Return the current NEW_PROJECTS dictionary
        """
        return NEW_PROJECTS


# shows a list of all permits
class Companies(Resource):
    # @auth.login_required
    def get(self):
        """Return the current companies database
        """
        return COMPANIES


# Setup the Api resource routing here
# Route the URL to the resource
# api.add_resource(Permit_LandUse, '/')
api.add_resource(Permit_LandUse, '/permits/landuse')
api.add_resource(Permit_Building, '/permits/building')
api.add_resource(Permit_Electrical, '/permits/electrical')
api.add_resource(Permit_Trade, '/permits/trade')
api.add_resource(NewProjectsList, '/new')
api.add_resource(Companies, '/companies')


if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
