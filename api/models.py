# api/models.py
"""Models for graphene API
"""
# from datetime import datetime
from mongoengine import (
    # Document,
    DynamicDocument,
    EmbeddedDocument
    )
from mongoengine.fields import (
    DateTimeField,
    EmbeddedDocumentField,
    # ListField,
    # ReferenceField,
    StringField,
    IntField,
    FloatField,
    # DictField,
    # MapField,
)


# class Coordinates(EmbeddedDocument):
#     longitude = FloatField()
#     latitude = FloatField()


class Location(EmbeddedDocument):

    type = StringField()
    coordinates = StringField()
    # coordinates is in a list but cannot be queried as an embedded document
    # coordinates = EmbeddedDocumentField(Coordinates)


class Permit(DynamicDocument):

    meta = {'collection': 'land_use'}
    permitnum = StringField()
    permitclass = StringField()
    permitclassmapped = StringField()
    permittypemapped = StringField()
    # applieddate = DateTimeField()  datetime does not work yet as a filter
    applieddate = StringField(required=False)
    location_1 = EmbeddedDocumentField(Location)
    location_1_address = StringField()
    location_1_city = StringField()
    location_1_state = StringField()
    location_1_zip = IntField()
    longitude = FloatField()
    latitude = FloatField()
    description = StringField()
    statuscurrent = StringField()


# class Building(Document):
#
#     meta = {'collection': 'building'}
