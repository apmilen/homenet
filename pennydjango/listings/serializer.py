from rest_framework import serializers

from listings.models import Listing


# Serializers define the API representation.
class ListingSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source='default_image')
    neighborhood = serializers.CharField(source='get_neighborhood_display')
    pets = serializers.CharField(source='get_pets_display')

    class Meta:
        model = Listing
        fields = (
            'price', 'bedrooms', 'bathrooms', 'address',
            'neighborhood', 'pets', 'image'
        )
