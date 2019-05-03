from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from django_select2.forms import Select2Widget

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


class UserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False, widget=forms.FileInput)
    first_name = forms.CharField(label='Name', required=False)

    class Meta:
        model = User
        fields = ('avatar', 'first_name')


class AvailabilityForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()

        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and start_time.hour >= end_time.hour:
            st_str = start_time.strftime('%H:%M')
            error_msg = f"Ending time must be later than {st_str}"
            self.add_error('end_time', error_msg)

        return cleaned_data

    class Meta:
        model = Availability
        exclude = ("agent", )
        widgets = {
            'neighborhood': Select2Widget
        }
