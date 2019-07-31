from django import forms
from django.core.exceptions import ValidationError

from job_applications.models import JobApplication
from penny.models import User


class JobApplicationForm(forms.ModelForm):

    class Meta:
        model = JobApplication
        fields = (
            'name', 'last_name', 'email', 'phone_number', 'current_company', 'position', 'resume',
        )
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if not email:
            raise ValidationError(
                'Email cannot be empty'
            )
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError(
                'That email is already in use'
            )
        return email
