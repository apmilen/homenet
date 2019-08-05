from django import forms

from payments.models import Transaction


class ManualTransactionForm(forms.ModelForm):
    
    class Meta:
        model = Transaction
        fields = ['lease_member', 'entered_by', 'amount', 'from_to', 'payment_method']

