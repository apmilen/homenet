from django import forms

from .models import RentProperty


class CreateRentPropertyForm(forms.ModelForm):
    price = forms.IntegerField(min_value=0)
    contact = forms.CharField(max_length=255)
    address = forms.CharField(max_length=255)
    latitude = forms.DecimalField()
    longitude = forms.DecimalField()

    about = forms.CharField(
        label='Description',
        max_length=512,
        required=False
    )

    bedrooms = forms.IntegerField(label='Number of bedrooms', initial=0)
    baths = forms.IntegerField(label='Number of baths', initial=0)
    pets_allowed = forms.BooleanField(required=False, initial=True)

    amenities = forms.CharField(label='Amenities description', required=False)

    class Meta:
        model = RentProperty
        exclude = ("publisher", )
