import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from penny.utils import get_output_fields
from rentals.models import RentProperty


class RentPropertyType(DjangoObjectType):
    class Meta:
        model = RentProperty
        filter_fields = ("bedrooms", "publisher")
        interfaces = (graphene.relay.Node,)


class Query(object):
    rentproperty = graphene.Field(RentPropertyType, id=graphene.UUID())
    all_rentp = DjangoFilterConnectionField(RentPropertyType)

    @staticmethod
    def resolve_all_rentp(root, info, **kwargs):
        output_fields = get_output_fields(info)
        query = RentProperty.objects.all()
        return query.only(*output_fields)

    @staticmethod
    def resolve_rentproperty(root, info, **kwargs):
        rp_id = kwargs.get("id")
        if rp_id:
            return RentProperty.objects.get(id=rp_id)
        return RentProperty.objects.none()
