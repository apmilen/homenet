import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from penny.utils import get_output_fields
from .models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = ("model_id", "username")
        interfaces = (graphene.relay.Node,)


class Query(object):
    user = graphene.Field(UserType, model_id=graphene.UUID())
    all_users = DjangoFilterConnectionField(UserType)

    @staticmethod
    def resolve_all_users(root, info, **kwargs):
        output_fields = get_output_fields(info)
        query = User.objects.all()
        return query.only(*output_fields)

    @staticmethod
    def resolve_user(root, info, **kwargs):
        user_id = kwargs.get("model_id")
        if user_id:
            return User.objects.get(model_id=user_id)
        return User.objects.none()
