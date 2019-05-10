from django.urls import path

from ui.views.pages import Home
from ui.views.accounts import Signup, UserProfile


urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('user/<username>/', UserProfile.as_view(), name="userprofile"),
    path('signup', Signup.as_view(), name='signup'),
]
