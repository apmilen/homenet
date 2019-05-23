from django import forms

from django_select2.forms import Select2Widget, Select2MultipleWidget

from .models import Listing, ListingDetail, ListingPhotos, Amenity
from penny.constants import AGENT_TYPE
from penny.models import User
from penny.widgets import GooglePointFieldWidgetJQuery


class ListingForm(forms.ModelForm):
    listing_agent = forms.ModelChoiceField(
        widget=Select2Widget,
        queryset=User.objects.filter(user_type=AGENT_TYPE)
    )
    sales_agent = forms.ModelChoiceField(
        widget=Select2Widget,
        queryset=User.objects.filter(user_type=AGENT_TYPE)
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].widget.attrs.update({'addon_before': '$'})
        self.fields['owner_pays'].widget.attrs.update({'addon_before': '%'})
        self.fields['size'].widget.attrs.update({'addon_after': 'sq.feet'})
        self.fields['date_available'].widget.attrs.update({
            'addon_before': '&#x1F4C5;'
        })
        self.fields['bathrooms'].widget.attrs.update({'step': '0.5'})
        self.fields['bedrooms'].widget.attrs.update({'step': '0.5'})

    class Meta:
        model = Listing
        fields = (
            'listing_type', 'price', 'move_in_cost', 'owner_pays',
            'agent_bonus', 'no_fee_listing', 'description', 'agent_notes',
            'utilities', 'size', 'bathrooms', 'bedrooms', 'date_available',
            'term', 'pets', 'address', 'geopoint', 'unit_number',
            'neighborhood', 'listing_agent', 'sales_agent'
        )
        widgets = {
            'address': forms.HiddenInput,
            'geopoint': GooglePointFieldWidgetJQuery,
            'listing_type': Select2Widget,
            'neighborhood': Select2Widget
        }


class ListingDetailForm(forms.ModelForm):
    amenities = forms.ModelMultipleChoiceField(
        widget=Select2MultipleWidget(attrs={'data-close-on-select': 'false'}),
        queryset=Amenity.objects.all(),
    )

    class Meta:
        model = ListingDetail
        fields = (
            'amenities', 'vacant', 'landlord_contact', 'building_access', 'hpd',
            'accepts_site_apply', 'listing_agreement', 'floorplans',
            'exclusive', 'private',  # 'office'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['listing_agreement'].required = False
        self.fields['floorplans'].required = False


class ListingPhotosForm(forms.ModelForm):

    class Meta:
        model = ListingPhotos
        fields = ('primary_photo', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['primary_photo'].required = False
