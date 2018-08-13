# api/schema.py
"""Set up the schema for the data.

The Relay node-edge interface is not currently used and are commented out.
"""
import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType

from models import Permit as PermitModel
from models import Location as LocationModel
# from models import Coordinates as CoordinatesModel


class Permit(MongoengineObjectType):
    """A permit application from Seattle Open Data"""
    class Meta:
        model = PermitModel
        interfaces = (Node,)
        # filter_fields = ['permitclass']


class Location(MongoengineObjectType):
    """Dictionary for location data from permit data"""
    class Meta:
        model = LocationModel
        interfaces = (Node,)


class Query(graphene.ObjectType):
    """Query class for permits"""
    # alternative for using node-edge interface
    node = Node.Field()
    permits_graph = MongoengineConnectionField(Permit)

    # alternative for using list interface
    permits = graphene.List(Permit)

    def resolve_permits(self, info):
        return list(PermitModel.objects.all())


schema = graphene.Schema(query=Query, types=[Permit])
