from flask import Flask
from flask_restful import Api, Resource
# reqparse,
# abort,

import json

app = Flask(__name__)
api = Api(app)


with open('../data/commercial.json', 'r') as f:
    PERMITS = json.load(f)


# shows a list of all permits
class PermitList(Resource):
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


# Setup the Api resource routing here
# Route the URL to the resource
api.add_resource(PermitList, '/')


if __name__ == '__main__':
    app.run(debug=True)
