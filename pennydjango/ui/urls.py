from django.urls import path

from ui.views.pages import Home, Schedule, ScheduleDelete
from ui.views.accounts import Signup, UserProfile


urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('schedule', Schedule.as_view(), name='schedule'),
    path('schedule/delete/<uuid:pk>',
         ScheduleDelete.as_view(), name='schedule-delete'),
    path('user/<username>/', UserProfile.as_view(), name="userprofile"),
    path('signup', Signup.as_view(), name='signup'),
]
