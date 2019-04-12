import graphene
from graphene_django.types import DjangoObjectType

from .models import RentProperty


class RentPropertyType(DjangoObjectType):
    class Meta:
        model = RentProperty


class Query(object):
    all_rentp = graphene.List(RentPropertyType)

    def resolve_all_rentp(self, info, **kwargs):
        return RentProperty.objects.all()
