from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from penny.models import User, Availability


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                'That email is already in use with a different account'
            )
        return email


class RentPropertyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.address


class AvailabilityForm(forms.ModelForm):

    class Meta:
        model = Availability
        exclude = ("agent", )