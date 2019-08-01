from django.urls import path

from payments.views import PaymentPage, ManualTransaction

urlpatterns = [
    path('<uuid:pk>/payments', PaymentPage.as_view(), name='payments'),
    path(
        'manual-transaction', 
        ManualTransaction.as_view(), 
        name='manual-transaction'
    ),
]
