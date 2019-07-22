# Serializers define the API representation.
from rest_framework import serializers

from penny.models import User


class AgentSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'avatar_url', 'first_name', 'last_name', 'profile_link', 'phone',
            'email', 'get_full_name'
        )
