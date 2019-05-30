# Serializers define the API representation.
from rest_framework import serializers

from listings.models import Listing, ListingDetail
from penny.models import User


class AgentSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'avatar_url', 'first_name', 'last_name', 'profile_link'
        )


class DetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ListingDetail
        fields = (
            'vacant', 'landlord_contact'
        )


class PublicListingSerializer(serializers.ModelSerializer):
    neighborhood = serializers.CharField(source='get_neighborhood_display')
    pets = serializers.CharField(source='get_pets_display')
    sales_agent = AgentSerializer()

    class Meta:
        model = Listing
        fields = (
            'address', 'amenities', 'bathrooms', 'bedrooms', 'default_image',
            'description', 'id', 'images', 'latitude', 'longitude',
            'neighborhood', 'no_fee_listing', 'pets', 'price', 'sales_agent'
        )


class PrivateListingSerializer(serializers.ModelSerializer):
    neighborhood = serializers.CharField(source='get_neighborhood_display')
    pets = serializers.CharField(source='get_pets_display')
    detail = DetailSerializer()
    sales_agent = AgentSerializer()
    listing_agent = AgentSerializer()

    class Meta:
        model = Listing
        fields = (
            'address', 'agent_bonus', 'agent_notes', 'amenities', 'bathrooms',
            'bedrooms', 'created', 'date_available', 'default_image',
            'description', 'detail', 'detail_link', 'edit_link',
            'full_address', 'images', 'listing_agent', 'modified',
            'move_in_cost', 'neighborhood', 'no_fee_listing', 'owner_pays',
            'pets', 'price', 'price_per_bed', 'sales_agent', 'short_id',
            'size', 'status', 'term', 'utilities',
        )
