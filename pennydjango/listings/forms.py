from django import forms

from django_select2.forms import Select2Widget, ModelSelect2Widget

from .models import Listing
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
            'agent_bonus', 'no_fee_listing', 'utilities', 'agent_notes',
            'description', 'bedrooms', 'bathrooms', 'size', 'date_available',
            'term', 'pets', 'address', 'geopoint', 'unit_number',
            'neighborhood', 'listing_agent', 'sales_agent'
        )
        widgets = {
            'address': forms.HiddenInput,
            'geopoint': GooglePointFieldWidgetJQuery,
            'listing_type': Select2Widget,
            'neighborhood': Select2Widget
        }
