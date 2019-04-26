from django.urls import path

from ui.views.pages import Home, Schedule, ScheduleDelete
from ui.views.accounts import Signup

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('schedule', Schedule.as_view(), name='schedule'),
    path('schedule/delete/<uuid:pk>',
         ScheduleDelete.as_view(), name='schedule-delete'),
    path('signup', Signup.as_view(), name='signup'),
]
