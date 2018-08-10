# api/models.py
# from datetime import datetime
from mongoengine import (
    # Document,
    DynamicDocument,
    EmbeddedDocument
    )
from mongoengine.fields import (
    DateTimeField,
    EmbeddedDocumentField,
    ListField,
    ReferenceField,
    StringField,
    # IntField,
    # FloatField,
    DictField,
    MapField
)


# class Coordinates(EmbeddedDocument):
#     longitude = StringField()
#     latitude = StringField()


class Location(EmbeddedDocument):

    type = StringField()
    coordinates = StringField()
    # coordinates = EmbeddedDocumentField(Coordinates)


class Permit(DynamicDocument):

    meta = {'collection': 'land_use'}
    permitnum = StringField()
    permitclass = StringField()
    applieddate = DateTimeField()
    location_1 = EmbeddedDocumentField(Location)


# class Building(Document):
#
#     meta = {'collection': 'building'}
