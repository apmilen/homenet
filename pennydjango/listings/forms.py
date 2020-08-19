from django import forms

from django_select2.forms import Select2Widget, Select2MultipleWidget

from .models import Listing, ListingDetail, ListingPhotos, ListingPhoto, Amenity, TransitOptions
from penny.constants import AGENT_TYPE
from penny.models import User
from penny.widgets import MapGeopoint


class ListingForm(forms.ModelForm):
    listing_agent = forms.ModelChoiceField(
        widget=Select2Widget,
        queryset=User.objects.filter(user_type=AGENT_TYPE)
    )
    nearby_transit = forms.ModelMultipleChoiceField(
        widget=Select2MultipleWidget(attrs={'data-close-on-select': 'false'}),
        queryset=TransitOptions.objects.all(),
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
        self.fields['address'].widget.attrs.update({'readonly': True})
        self.fields['other_nearby_transit'].required = False

    class Meta:
        model = Listing
        fields = (
            'listing_type', 'price', 'move_in_cost', 'owner_pays',
            'agent_bonus', 'no_fee_listing', 'description', 'agent_notes',
            'utilities', 'size', 'bathrooms', 'bedrooms', 'date_available',
            'term', 'pets', 'address', 'geopoint', 'nearby_transit', 'other_nearby_transit',
            'unit_number', 'neighborhood', 'listing_agent', 'parking',
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
            'floorplans', 'vacant', 'hpd', 'exclusive', 'private',
            'accepts_site_apply', # 'office'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
