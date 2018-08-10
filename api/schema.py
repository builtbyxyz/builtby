import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType

from models import Permit as PermitModel
from models import Location as LocationModel
# from models import Coordinates as CoordinatesModel


class Permit(MongoengineObjectType):

    class Meta:
        model = PermitModel
        interfaces = (Node,)


class Location(MongoengineObjectType):

    class Meta:
        model = LocationModel
        interfaces = (Node,)


# class Coordinates(MongoengineObjectType):
#
#     class Meta:
#         model = CoordinatesModel
#         interfaces = (Node,)


class Query(graphene.ObjectType):
    node = Node.Field()
    all_permits = MongoengineConnectionField(Permit)


schema = graphene.Schema(query=Query, types=[Permit])
