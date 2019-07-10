from django.urls import path

from payments.views import PaymentPage

urlpatterns = [
    path('<uuid:pk>/payments', PaymentPage.as_view(), name='payments'),
]