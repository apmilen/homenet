from django.urls import path

from ui.views.pages import Home

urlpatterns = [
    path('', Home.as_view())
]
