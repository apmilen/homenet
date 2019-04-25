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
        queryset=RentProperty.objects.filter(is_listed=True)
    )
    start_datetime = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    end_datetime = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])

    class Meta:
        model = Availability
        exclude = ("agent", )
