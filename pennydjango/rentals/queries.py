import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField


from .models import RentProperty


class RentPropertyType(DjangoObjectType):
    class Meta:
        model = RentProperty
        filter_fields = ("bedrooms", "publisher")
        interfaces = (graphene.relay.Node,)


class Query(object):
    rentproperty = graphene.Field(RentPropertyType, model_id=graphene.UUID())
    all_rentp = DjangoFilterConnectionField(RentPropertyType)

    @staticmethod
    def resolve_all_rentp(root, info, **kwargs):
        return RentProperty.objects.select_related('publisher').all()

    @staticmethod
    def resolve_rentproperty(root, info, **kwargs):
        rp_id = kwargs.get("model_id")
        if rp_id:
            return RentProperty.objects.get(model_id=rp_id)
        return RentProperty.objects.none()
