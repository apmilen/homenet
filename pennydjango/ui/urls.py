from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from ui.views.pages import Home, Schedule
from ui.views.accounts import Signup

urlpatterns = [
    path('', Home.as_view()),
    path('schedule', Schedule.as_view(), name='schedule'),
    path('signup', Signup.as_view(), name='signup'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
