import graphene

from graphene_django.types import DjangoObjectType
from graphene_django.debug import DjangoDebug

from rentals.models import RentProperty


class RentPropertyType(DjangoObjectType):
    pk = graphene.UUID(source='id')

    class Meta:
        model = RentProperty

        filter_fields = ("id", "bedrooms", "publisher")
        interfaces = (graphene.Node,)


class Query(graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')

    rentproperty = graphene.Field(RentPropertyType, id=graphene.UUID())
    rentpropertys = graphene.List(RentPropertyType)

    def resolve_rentproperty(self, info, **kwargs):
        if kwargs:
            return RentProperty.objects.get(**kwargs)
        return None

    def resolve_rentpropertys(self, info, **kwargs):
        return RentProperty.objects.all().filter(**kwargs)


# class Mutation(graphene.ObjectType):
#     pass


schema = graphene.Schema(query=Query)
