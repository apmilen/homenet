from django.http import JsonResponse

from ui.views.base_views import PublicReactView

from penny.models import User
from penny.mixins import AdminRequiredMixin
from penny.constants import USER_TYPE


class Users(AdminRequiredMixin, PublicReactView):
    title = "Users"
    component = 'pages/users.js'

    def props(self, request, *args, **kwargs):
        query_filter = {'is_active': True}

        users = User.objects.filter(**query_filter)

        return {
            'users': [user.__json__() for user in users],
            'user_types': USER_TYPE,
        }

    def post(self, request, *args, **kwargs):
        request_type = request.POST.get('type')
        response = {'success': False, 'details': "My job is done"}

        if request_type == 'NEW_USER':
            name = request.POST.get('name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            user_type = request.POST.get('user_type')
            response = invite_new_user(name, username, email, user_type)

        return JsonResponse(response)


def invite_new_user(name, username, email, user_type):
    if not (email and user_type):
        return {
            'success': False,
            'details': "Missing required data"
        }

    qs = User.objects.filter(email=email)
    if qs.exists():
        return {
            'success': False,
            'details': 'Email belongs to registered user. Try another one.'
        }

    new_user = User.objects.create_user(
        first_name=name,
        username=username or email,
        password='',
        email=email,
        user_type=user_type
    )

    return {
        'success': True,
        'new_user': new_user.__json__(),
    }
