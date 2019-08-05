from django.urls import path

from payments.views import PaymentPage, PaymentPagePlaid

urlpatterns = [
    path('<uuid:pk>/payments', PaymentPage.as_view(), name='payments'),
    path('<uuid:pk>/plaid', PaymentPagePlaid.as_view(), name='plaid'),
]