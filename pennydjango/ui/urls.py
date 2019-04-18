from django.urls import path

from ui.views.pages import Home
from ui.views.accounts import Signup

urlpatterns = [
    path('signup', Signup.as_view(), name='signup'),
    path('', Home.as_view())
]
