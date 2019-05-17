from django import forms

from django_select2.forms import Select2Widget, Select2MultipleWidget

from .models import Listing, ListingDetail, Amenity
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
        widget=Select2MultipleWidget,
        queryset=Amenity.objects.all(),
    )

    class Meta:
        model = ListingDetail
        fields = (
            'amenities', 'vacant', 'landlord_contact', 'building_access', 'hpd',
            'accepts_site_apply', 'listing_agreement', 'floorplans',
            'exclusive', 'private',  # 'office'
        )
