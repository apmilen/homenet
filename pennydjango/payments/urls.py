from django.urls import path

from . import views
from payments.views import PaymentPage

urlpatterns = [
    path('<uuid:pk>/payments', PaymentPage.as_view(), name='payments'),
]