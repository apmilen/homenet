from graphene import relay, ObjectType, Schema, Field
from graphene_django.types import DjangoObjectType
from graphene_django.debug import DjangoDebug

import rentals.queries
import rentals.mutations

from .models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = ("id", "name")
        interfaces = (relay.Node,)


class Query(rentals.queries.Query, ObjectType):
    debug = Field(DjangoDebug, name='__debug')


class Mutation(rentals.mutations.Mutation, ObjectType):
    pass


schema = Schema(query=Query, mutation=Mutation)
