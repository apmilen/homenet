import graphene

from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.fields import DjangoConnectionField

from rentals.models import RentProperty


class RentPropertyType(DjangoObjectType):
    pk = graphene.UUID(source='id')

    class Meta:
        model = RentProperty

        filter_fields = ("id", "bedrooms", "publisher")
        interfaces = (graphene.relay.Node,)


class RentalsQueries(graphene.ObjectType):
    rentproperty = DjangoConnectionField(RentPropertyType)
    rentpropertys = DjangoFilterConnectionField(RentPropertyType)
