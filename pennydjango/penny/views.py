from ui.views.base_views import PublicReactView

from penny.models import User


class Users(PublicReactView):
    title = "Users"
    component = 'pages/users.js'

    def props(self, request, *args, **kwargs):
        query_filter = {'is_active': True}

        users = User.objects.filter(**query_filter)

        return {
            'users': [user.__json__() for user in users]
        }
