from django.urls import path

from ui.views.accounts import Signup, UserProfile


urlpatterns = [
    path('user/<username>/', UserProfile.as_view(), name="userprofile"),
    path('signup', Signup.as_view(), name='signup'),
]
