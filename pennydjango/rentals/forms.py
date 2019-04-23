from django import forms

from .models import RentProperty, Availability


class CreateRentPropertyForm(forms.ModelForm):
    class Meta:
        model = RentProperty
        exclude = ("publisher", )


class RentPropertyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.address


class AvailabilityForm(forms.ModelForm):
    reference_property = RentPropertyModelChoiceField(
        queryset=RentProperty.objects.all()
    )

    class Meta:
        model = Availability
        exclude = ("agent", )
