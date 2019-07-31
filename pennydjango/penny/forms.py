from email.utils import parseaddr

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from penny.models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            'email', 'first_name', 'last_name'
        )

    def clean_email(self):
        _, email = parseaddr(self.cleaned_data.get('email'))

        if '@' not in email:
            raise ValidationError(
                'Email is invalid, double check it and try again'
            )
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError(
                'That email is already in use with a different account'
            )
        return email


class UserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False, widget=forms.FileInput)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name')


class GeneralSettingsForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'bio')
