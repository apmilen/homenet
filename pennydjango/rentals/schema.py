import graphene
from graphene_django.types import DjangoObjectType

from .models import RentProperty


class RentPropertyType(DjangoObjectType):
    class Meta:
        model = RentProperty


class Query(object):
    rentproperty = graphene.Field(RentPropertyType,
                                  required=True,
                                  id=graphene.UUID())

    all_rentp = graphene.List(RentPropertyType)

    def resolve_all_rentp(self, info, **kwargs):
        return RentProperty.objects.select_related('publisher').all()

    def resolve_rentproperty(self, **kwargs):
        rp_id = kwargs.get("id")
        if rp_id:
            return RentProperty.objects.get(id=rp_id)
        return RentProperty.objects.none()
