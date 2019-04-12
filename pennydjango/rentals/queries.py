import graphene
from graphene_django.types import DjangoObjectType

from .models import RentProperty


class RentPropertyType(DjangoObjectType):
    class Meta:
        model = RentProperty


class Query(object):
    rentproperty = graphene.Field(RentPropertyType,
                                  required=True,
                                  id=graphene.ID())

    all_rentp = graphene.List(RentPropertyType)

    @staticmethod
    def resolve_all_rentp(root, info):
        return RentProperty.objects.select_related('publisher').all()

    @staticmethod
    def resolve_rentproperty(root, info, **kwargs):
        rp_id = kwargs.get("id")
        if rp_id:
            return RentProperty.objects.get(id=rp_id)
        return RentProperty.objects.none()
