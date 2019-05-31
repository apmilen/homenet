from rest_framework import serializers

from listings.serializer import ListingSerializer
from leases.models import Lease


# Serializers define the API representation.
class LeaseSerializer(serializers.ModelSerializer):
    listing = ListingSerializer()
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Lease
        fields = (
            'id', 'short_id', 'listing', 'offer', 'length_of_lease',
            'move_in_date', 'op', 'total_broker_fee', 'status', 'created_by',
            'created', 'modified'
        )
