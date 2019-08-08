from django.urls import path

from penny.views import (
    Users, GeneralSettingsView, PasswordSettingsView
)


urlpatterns = [
    path('users/', Users.as_view(), name='users'),
    # path('users-list', UsersList.as_view(), name='users_list'),
    path('user/settings', GeneralSettingsView.as_view(), name='user_settings'),
    path('user/password', PasswordSettingsView.as_view(), name='user_password'),
]
