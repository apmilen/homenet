from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from penny.models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label='Your Name')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name')

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


class UserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False, widget=forms.FileInput)
    first_name = forms.CharField(label='Name', required=False)

    class Meta:
        model = User
        fields = ('avatar', 'first_name')
