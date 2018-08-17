from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api, Resource
# reqparse,
# abort,
from pymongo import MongoClient
import json


app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

USER_DATA = {
    'admin': 'builtby2018'
}

with open('../data/commercial.json', 'r') as f:
    PERMITS = json.load(f)

mc = MongoClient('localhost', 27017)
db = mc['builtby']
COMPANIES = list(db['companies_20180816'].find())

# convert mongo objectid object to string for json serialization
for company in COMPANIES:
    company['_id'] = str(company['_id'])


@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password


# shows a list of all permits
class PermitList(Resource):
    # @auth.login_required
    def get(self):
        """Return the current TODO dictionary

        Example:
            # In the terminal
            $ curl http://localhost:5000/

            OR

            # Python
            requests.get('http://localhost:5000/').json()
        """
        return PERMITS


# shows a list of all permits
class Companies(Resource):
    # @auth.login_required
    def get(self):
        """Return the current TODO dictionary

        Example:
            # In the terminal
            $ curl http://localhost:5000/companies

            OR

            # Python
            requests.get('http://localhost:5000/companies').json()
        """
        return COMPANIES


# Setup the Api resource routing here
# Route the URL to the resource
api.add_resource(PermitList, '/')
api.add_resource(Companies, '/companies')


if __name__ == '__main__':
    app.run(debug=True)
