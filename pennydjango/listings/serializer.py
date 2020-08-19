# Serializers define the API representation.

from rest_framework import serializers

from listings.models import Listing, ListingDetail
from penny.serializers import AgentSerializer


class DetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ListingDetail
        fields = (
            'vacant', 'landlord_contact'
        )


class PublicListingSerializer(serializers.ModelSerializer):
    neighborhood = serializers.CharField(source='get_neighborhood_display')
    pets = serializers.CharField(source='get_pets_display')
    parking = serializers.CharField(source='get_parking_display')
    nearby_transit = serializers.StringRelatedField(many=True)

    class Meta:
        model = Listing
        fields = (
            'address', 'amenities', 'bathrooms', 'bedrooms', 'default_image',
            'description', 'id', 'images', 'latitude', 'longitude',
            'neighborhood', 'no_fee_listing', 'pets', 'price', 'created', 'parking', 
            'nearby_transit', 'other_nearby_transit','detail_link', 'edit_link',
            'photos_link', 'change_status_link', 'offer_link', 'listing_link'
        )


class PrivateListingSerializer(serializers.ModelSerializer):
    neighborhood = serializers.CharField(source='get_neighborhood_display')
    pets = serializers.CharField(source='get_pets_display')
    move_in_cost = serializers.CharField(source='get_move_in_cost_display')
    status = serializers.CharField(source='get_status_display')
    parking = serializers.CharField(source='get_parking_display')
    detail = DetailSerializer()
    listing_agent = AgentSerializer()
    nearby_transit = serializers.StringRelatedField(many=True)

    class Meta:
        model = Listing
        fields = (
            'address', 'agent_bonus', 'agent_notes', 'amenities', 'bathrooms',
            'bedrooms', 'created', 'date_available', 'default_image',
            'description', 'detail', 'detail_link', 'edit_link', 'photos_link',
            'full_address', 'images', 'listing_agent', 'modified',
            'move_in_cost', 'neighborhood', 'no_fee_listing', 'owner_pays',
            'pets', 'price', 'price_per_bed', 'short_id', 'id','size', 'status',
            'term', 'utilities', 'listing_link', 'offer_link', 'nearby_transit',
            'other_nearby_transit', 'parking', 'collections', 'change_status_link',
        )
