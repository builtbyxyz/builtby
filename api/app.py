from database import init_db
from flask import Flask
from flask_graphql import GraphQLView
from schema import schema


app = Flask(__name__)
app.debug = True


default_query = """
{
    allPermits (applieddate: "2018-07-13") {
        edges {
            node {
                id,
                permitnum,
                applieddate,
                location1 {
                    type,
                    coordinates
                }
            }
        }
    }
}
"""


app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql',
                 schema=schema, graphiql=True))


if __name__ == '__main__':
    init_db()
    app.run()
