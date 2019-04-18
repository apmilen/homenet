import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from penny.utils import get_output_fields
from rentals.models import RentProperty


class RentPropertyType(DjangoObjectType):
    pk = graphene.UUID(source='id')

    class Meta:
        model = RentProperty

        filter_fields = ("bedrooms", "publisher")
        interfaces = (graphene.Node,)


class Query(graphene.ObjectType):
    rent_property = graphene.Field(RentPropertyType, id=graphene.UUID())
    all_rent_property = graphene.List(RentPropertyType)

    def resolve_rent_property(self, info, **kwargs):
        row_id = kwargs.get('id')

        if row_id is not None:
            return RentProperty.objects.get(id=row_id)

        return None

    def resolve_all_rent_property(self, info, **kwargs):
        return RentProperty.objects.all()
