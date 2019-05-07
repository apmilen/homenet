import json
import graphene

from .queries import RentPropertyType
from rentals.forms import RentPropertyForm


class RentPropertyInput(graphene.InputObjectType):
    price = graphene.Int(required=True)
    contact = graphene.String(required=True)
    address = graphene.String(required=True)
    latitude = graphene.Float(required=True)
    longitude = graphene.Float(required=True)
    about = graphene.String()
    bedrooms = graphene.Int(required=True)
    baths = graphene.Int(required=True)
    pets_allowed = graphene.Boolean()
    amenities = graphene.String(required=True)


class CreateRentPropertyMutation(graphene.relay.ClientIDMutation):
    class Input:
        rentproperty = RentPropertyInput(required=True)

    status = graphene.Int()
    form_errors = graphene.String()
    rentproperty = graphene.Field(RentPropertyType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        if not info.context.user.is_authenticated:
            return CreateRentPropertyMutation(status=403)

        data = kwargs.get("rentproperty")
        form = RentPropertyForm(data=data)
        # Here we would usually use Django forms to validate the input
        if not form.is_valid():
            return CreateRentPropertyMutation(
                status=400,
                form_errors=json.dumps(form.errors)
            )

        obj = form.save(commit=False)
        obj.publisher = info.context.user
        obj.save()
        return CreateRentPropertyMutation(status=200, rentproperty=obj)


class Mutation(graphene.ObjectType):
    create_rentproperty = CreateRentPropertyMutation.Field()
