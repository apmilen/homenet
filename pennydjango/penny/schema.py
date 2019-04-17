import graphql_jwt
from graphene import relay, ObjectType, Schema, Field
from graphene_django.types import DjangoObjectType
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
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = Schema(query=Query, mutation=Mutation)
