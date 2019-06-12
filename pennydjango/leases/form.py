from django import forms
from django.core.exceptions import ValidationError

from penny.models import User
from leases.constants import CHARGE_OPTIONS
from leases.models import Lease, LeaseMember, MoveInCost


class LeaseCreateForm(forms.ModelForm):

    class Meta:
        model = Lease
        fields = (
            'offer', 'length_of_lease', 'move_in_date', 'op', 'total_broker_fee'
        )


class BasicLeaseMemberForm(forms.ModelForm):
    class Meta:
        model = LeaseMember
        fields = ('name', 'email', 'applicant_type', 'app_fee')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError(
                'Email cannot be empty'
            )
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                'That email is already in use with a different account'
            )
        return email


class MoveInCostForm(forms.ModelForm):
    charge = forms.ChoiceField(choices=CHARGE_OPTIONS)

    class Meta:
        model = MoveInCost
        fields = ('value', 'charge')

    class Media:
        js = ('js/move-in-costs.js', )

    def __init__(self, *args, pk=None, **kwargs):
        super().__init__(*args, **kwargs)
        if pk is not None:
            options = CHARGE_OPTIONS.copy()
            members_offer = LeaseMember.objects.filter(offer_id=pk)\
                                               .filter(user__isnull=False)\
                                               .select_related('user')\
                                               .only('user__first_name')

            for member in members_offer:
                first_name = member.user.first_name
                options.append(
                    (f"{first_name}'s Application Fee",
                     f"{first_name}'s Application Fee")
                )
            self.fields['charge'].widget.choices = options
