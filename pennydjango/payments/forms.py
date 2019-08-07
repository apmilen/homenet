from django import forms

from payments.models import Transaction
from payments.constants import MANUAL_TRANSACTION_CHOICES

class ManualTransactionForm(forms.ModelForm):
    from_to = forms.ChoiceField(choices=MANUAL_TRANSACTION_CHOICES)

    class Meta:
        model = Transaction
        fields = [
            'from_to', 
            'lease_member', 
            'amount', 
            'payment_method'
        ]
