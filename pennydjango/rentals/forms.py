from django import forms

from .models import RentProperty


class CreateRentPropertyForm(forms.ModelForm):
    class Meta:
        model = RentProperty
        exclude = ("publisher", )
