from django import forms

from django_select2.forms import Select2Widget
from job_applications.models import JobApplication


class JobApplicationForm(forms.ModelForm):

    class Meta:
        model = JobApplication
        fields = (
            'name', 'last_name', 'email', 'phone_number', 'current_company', 'position', 'resume',
        )