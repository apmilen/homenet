import graphene

from graphene_django.types import DjangoObjectType
from graphene_django.debug import DjangoDebug

from .models import User


class UserType(DjangoObjectType):
    pk = graphene.UUID(source='id')

    class Meta:
        model = User

        filter_fields = ("id", "username", "email")
        interfaces = (graphene.Node,)


class Query(graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')

    user = graphene.Field(UserType, id=graphene.UUID(), username=graphene.String())
    users = graphene.List(UserType, username=graphene.String())

    def resolve_user(self, info, **kwargs):
        if kwargs:
            return User.objects.get(**kwargs)
        return None

    def resolve_users(self, info, **kwargs):
        return User.objects.all().filter(**kwargs)


# class Mutation(graphene.ObjectType):
#     pass


schema = graphene.Schema(query=Query)
