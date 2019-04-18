import graphene

from penny.schema import PennyQueries
from rentals.schema import RentalsQueries
from graphene_django.debug import DjangoDebug


class RootQuery(PennyQueries, RentalsQueries, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')


schema = graphene.Schema(query=RootQuery)
