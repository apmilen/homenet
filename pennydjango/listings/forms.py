from django import forms

from django_select2.forms import Select2Widget, Select2MultipleWidget

from .models import Listing, ListingDetail, ListingPhotos, ListingPhoto, Amenity
from penny.constants import AGENT_TYPE
from penny.models import User
from penny.widgets import MapGeopoint


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
        self.fields['size'].widget.attrs.update({'addon_after': 'sq.feet', "required": False})
        self.fields['size'].required = False
        self.fields['date_available'].widget.attrs.update({
            'addon_before': '&#x1F4C5;'
        })
        self.fields['agent_bonus'].widget.attrs.update({'addon_before': '$'})
        self.fields['bathrooms'].widget.attrs.update({'step': '0.5'})
        self.fields['bedrooms'].widget.attrs.update({'step': '0.5'})
        self.fields['walkability_score'].widget.attrs.update({'addon_before': '%'})
        self.fields['bikeability_score'].widget.attrs.update({'addon_before': '%'})
        self.fields['address'].widget.attrs.update({'readonly': True})

    class Meta:
        model = Listing
        fields = (
            'listing_type', 'price', 'move_in_cost', 'owner_pays',
            'agent_bonus', 'no_fee_listing', 'description', 'agent_notes',
            'utilities', 'size', 'bathrooms', 'bedrooms', 'date_available',
            'term', 'pets', 'address', 'geopoint', 'nearby_transit', 'unit_number',
            'neighborhood', 'listing_agent', 'sales_agent', 'walkability_score',
            'bikeability_score', 'parking'
        )
        widgets = {
            'geopoint': MapGeopoint,
            'listing_type': Select2Widget,
            'neighborhood': Select2Widget,
        }


class ListingDetailForm(forms.ModelForm):
    amenities = forms.ModelMultipleChoiceField(
        widget=Select2MultipleWidget(attrs={'data-close-on-select': 'false'}),
        queryset=Amenity.objects.all(),
    )

    class Meta:
        model = ListingDetail
        fields = (
            'amenities', 'landlord_contact', 'building_access',
            'listing_agreement', 'floorplans', 'vacant', 'hpd', 'exclusive',
            'private', 'accepts_site_apply',  # 'office'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['listing_agreement'].required = False
        self.fields['floorplans'].required = False


class ListingPhotosForm(forms.ModelForm):

    class Meta:
        model = ListingPhotos
        fields = ('primary_photo', )


class SingleListingPhotoForm(forms.ModelForm):

    class Meta:
        model = ListingPhoto
        fields = ('photo', )


ListingPhotoFormSet = forms.modelformset_factory(
    ListingPhoto,
    form=SingleListingPhotoForm,
    extra=3
)


class ChangeListingStatusForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = ('status', )
