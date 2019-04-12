import graphene
from graphene_django.types import DjangoObjectType

import rentals.schema

from .models import User


class CategoryType(DjangoObjectType):
    class Meta:
        model = User


class Query(rentals.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
