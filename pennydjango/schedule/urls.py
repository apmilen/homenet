from django.urls import path

from schedule.views import Schedule, ScheduleDelete


urlpatterns = [
    path('', Schedule.as_view(), name='schedule'),
    path('delete/<uuid:pk>',
         ScheduleDelete.as_view(), name='schedule-delete'),
]
