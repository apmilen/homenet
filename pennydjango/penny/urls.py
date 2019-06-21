from django.urls import path

from penny.views import UsersList, GeneralSettingsView, PasswordSettingsView


urlpatterns = [
    path('users-list', UsersList.as_view(), name='users_list'),
    path('user/settings', GeneralSettingsView.as_view(), name='user_settings'),
    path('user/password', PasswordSettingsView.as_view(), name='user_password'),
]
