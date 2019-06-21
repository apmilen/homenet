from django.urls import path, include

from penny.views import UsersList


urlpatterns = [
    path('users-list', UsersList.as_view(), name='users_list'),
]
