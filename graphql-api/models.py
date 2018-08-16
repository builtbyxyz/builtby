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

    meta = {'collection': 'commercial'}
    permit_num = StringField()
    permit_class = StringField()
    permit_class_mapped = StringField()
    # permittypemapped = StringField()
    # applieddate = DateTimeField()  datetime does not work yet as a filter
    applied_date = StringField(required=False)
    # location_1 = EmbeddedDocumentField(Location)
    address = StringField()
    city = StringField()
    state = StringField()
    zip = IntField()
    longitude = FloatField()
    latitude = FloatField()
    description = StringField()
    statuscurrent = StringField()


# class Building(Document):
#
#     meta = {'collection': 'building'}
