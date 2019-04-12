import graphene
from graphene_django.types import DjangoObjectType

import rentals.queries
import rentals.mutations

from .models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query(rentals.queries.Query, graphene.ObjectType):
    pass


class Mutation(rentals.mutations.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
