from rest_framework import serializers

from listings.models import Listing


# Serializers define the API representation.
class ListingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Listing
        fields = (
            'address', 'amenities_dict', 'bathrooms', 'bedrooms',
            'default_image', 'description', 'detail_link', 'edit_link', 'id',
            'images', 'latitude', 'longitude', 'neighborhood_name',
            'no_fee_listing', 'pets', 'price', 'sales_agent'
        )
