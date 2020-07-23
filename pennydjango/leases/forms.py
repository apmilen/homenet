from email.utils import parseaddr
from django import forms
from django.core.exceptions import ValidationError

from penny.models import User
from leases.constants import CHARGE_OPTIONS
from leases.models import Lease, LeaseMember, MoveInCost, RentalApplication, \
    RentalAppDocument


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
        _, email = parseaddr(self.cleaned_data.get('email'))
        email = email.strip()

        if '@' not in email:
            raise ValidationError(
                'Email is invalid, double check it and try again'
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
            self.fields['charge'] = forms.ChoiceField(choices=options)


class SignAgreementForm(forms.ModelForm):

    class Meta:
        model = LeaseMember
        fields = ('legal_name', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['legal_name'].required = True

    def clean_legal_name(self):
        legal_name = self.cleaned_data.get('legal_name')
        if not legal_name:
            raise ValidationError('legal_name cannot be empty')
        return legal_name


class RentalApplicationForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = RentalApplication
        fields = (
            'name', 'phone', 'date_of_birth', 'ssn', 'driver_license',
            'n_of_pets', 'current_address', 'current_monthly_rent',
            'landlord_name', 'landlord_contact', 'current_company',
            'job_title', 'annual_income', 'time_at_current_job'
        )

    def check_values(self, cleaned_data, required_fields):
        for value in required_fields:
            if not cleaned_data[value]:
                msg = f'{value.capitalize()} field is required.'
                raise ValidationError(msg)

    def clean(self):
        cleaned_data = super().clean()
        if not self.data['draft']:
            required_fields = ['name', 'phone', 'ssn']
            self.check_values(cleaned_data, required_fields)
        return cleaned_data


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['phone'].required = False
        self.fields['ssn'].required = False
        self.fields['date_of_birth'].required = False
        self.fields['driver_license'].required = False
        self.fields['n_of_pets'].required = False
        self.fields['current_address'].required = False
        self.fields['current_monthly_rent'].required = False
        self.fields['landlord_name'].required = False
        self.fields['landlord_contact'].required = False
        self.fields['current_company'].required = False
        self.fields['job_title'].required = False
        self.fields['annual_income'].required = False
        self.fields['time_at_current_job'].required = False

        self.fields['ssn'].label = "SSN"

class RentalApplicationEditingForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = RentalApplication
        fields = ('editing', )


class RentalAppDocForm(forms.ModelForm):

    class Meta:
        model = RentalAppDocument
        fields = ('file', )


class ChangeLeaseStatusForm(forms.ModelForm):

    class Meta:
        model = Lease
        fields = ('status', )
