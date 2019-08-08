from django.urls import path

from ui.views.accounts import Signup, UserProfile
from job_applications.views import JobApplication
from ui.views.pages import Home


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('user/<id>/', UserProfile.as_view(), name="userprofile"),
    path('signup', Signup.as_view(), name='signup'),
    path('jobs', JobApplication.as_view(), name='jobs'),
]
