from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from ui.views.pages import Home
from ui.views.accounts import Signup, UserProfile

urlpatterns = [
    path('signup', Signup.as_view(), name='signup'),
    path('', Home.as_view()),
    path('user/<username>/', UserProfile.as_view(), name="userprofile")
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
