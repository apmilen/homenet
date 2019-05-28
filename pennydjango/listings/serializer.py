# Serializers define the API representation.
from rest_framework import serializers

from listings.models import Listing
from penny.models import User


class SalesAgentSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'avatar_url', 'first_name'
        )


class ListingSerializer(serializers.ModelSerializer):
    neighborhood = serializers.CharField(source='get_neighborhood_display')
    pets = serializers.CharField(source='get_pets_display')
    sales_agent = SalesAgentSerializer()

    class Meta:
        model = Listing
        fields = (
            'address', 'amenities', 'bathrooms', 'bedrooms', 'default_image',
            'description', 'id', 'images', 'latitude', 'longitude',
            'neighborhood', 'no_fee_listing', 'pets', 'price', 'sales_agent'
        )
