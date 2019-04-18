import json
import graphene

from .forms import CustomUserCreationForm
from .queries import UserType


class CreateUser(graphene.relay.ClientIDMutation):
    class Input:
        username = graphene.String(required=True)
        password1 = graphene.String(required=True)
        password2 = graphene.String(required=True)
        email = graphene.String(required=True)
        # first_name = graphene.String(required=True)
        # last_name = graphene.String(required=True)

    user = graphene.Field(UserType)
    status = graphene.Int()
    form_errors = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        form = CustomUserCreationForm(data=kwargs)
        if not form.is_valid():
            return CreateUser(
                status=400,
                form_errors=json.dumps(form.errors)
            )
        new_user = form.save()
        return CreateUser(status=200, user=new_user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
