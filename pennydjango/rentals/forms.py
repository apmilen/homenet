from django import forms

from .models import RentProperty


class CreateRentPropertyForm(forms.ModelForm):
    is_listed = forms.BooleanField(
        label="Show listing",
        help_text="Uncheck to make it private (draft)."
    )

    class Meta:
        model = RentProperty
        exclude = ("publisher", )
