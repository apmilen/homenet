from django.urls import path

from payments.views import PaymentPage, ManualTransaction, PaymentPagePlaid

urlpatterns = [
    path('<uuid:pk>/payments', PaymentPage.as_view(), name='payments'),
    path('<uuid:pk>/plaid', PaymentPagePlaid.as_view(), name='plaid'),
    path(
        'manual-transaction', 
        ManualTransaction.as_view(), 
        name='manual-transaction'
    ),
]
