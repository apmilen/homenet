from django.urls import path

from ui.views.pages import Home, CreateRentProperty

urlpatterns = [
    path('', Home.as_view()),
    path('new_prop/', CreateRentProperty.as_view(), name='CreateRentProperty'),
]
