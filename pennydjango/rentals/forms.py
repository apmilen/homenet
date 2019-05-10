from django import forms

from rentals.models import RentProperty

from penny.widgets import TaggitInput, GooglePointFieldWidgetJQuery


class RentPropertyForm(forms.ModelForm):
    is_listed = forms.BooleanField(
        label="Show listing",
        initial=True,
        required=False,
        help_text="Uncheck to make it private (draft)."
    )

    class Meta:
        model = RentProperty
        fields = (
            "is_listed", "price", "contact", "address", "geopoint", "about",
            "bedrooms", "baths", "pets_allowed", "amenities"
        )
        widgets = {
            'address': forms.HiddenInput(),
            'geopoint': GooglePointFieldWidgetJQuery,
            'amenities': TaggitInput
        }
