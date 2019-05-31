from django import forms

from leases.models import Lease


class LeaseCreateForm(forms.ModelForm):

    class Meta:
        model = Lease
        fields = (
            'offer', 'length_of_lease', 'move_in_date', 'op', 'total_broker_fee'
        )
