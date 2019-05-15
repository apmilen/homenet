from django.urls import path, include

from ui.views.accounts import Signup, UserProfile


urlpatterns = [
    path('', include("rentals.urls")),
    path('user/<username>/', UserProfile.as_view(), name="userprofile"),
    path('signup', Signup.as_view(), name='signup'),
]
