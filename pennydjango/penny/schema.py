from graphene import relay, ObjectType, Schema
from graphene_django.types import DjangoObjectType

import rentals.queries
import rentals.mutations

from .models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = ("id", "name")
        interfaces = (relay.Node,)


class Query(rentals.queries.Query, ObjectType):
    pass


class Mutation(rentals.mutations.Mutation, ObjectType):
    pass


schema = Schema(query=Query, mutation=Mutation)
