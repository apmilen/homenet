from graphene import ObjectType, Schema, Field
from graphene_django.debug import DjangoDebug

import penny.mutations
import penny.queries
import rentals.queries
import rentals.mutations


class Query(rentals.queries.Query, penny.queries.Query, ObjectType):
    debug = Field(DjangoDebug, name='__debug')


class Mutation(rentals.mutations.Mutation,
               penny.mutations.Mutation,
               ObjectType):
    pass


schema = Schema(query=Query, mutation=Mutation)
