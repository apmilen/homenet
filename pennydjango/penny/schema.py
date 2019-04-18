import graphene

from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.fields import DjangoConnectionField

from .models import User


class UserType(DjangoObjectType):
    pk = graphene.UUID(source='id')

    class Meta:
        model = User

        filter_fields = ("id", "username", "email")
        interfaces = (graphene.relay.Node,)


class PennyQueries(graphene.ObjectType):
    user = DjangoConnectionField(UserType)
    users = DjangoFilterConnectionField(UserType)

