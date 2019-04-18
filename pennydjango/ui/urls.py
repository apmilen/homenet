from django.urls import path


from ui.views.pages import Home, CreateRentProperty
from ui.views.accounts import Signup

urlpatterns = [
    path('', Home.as_view()),
    path('signup', Signup.as_view(), name='signup'),
    path('new_prop/', CreateRentProperty.as_view(), name='CreateRentProperty'),
]
