from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.utils.translation import gettext_lazy as _

from .models import Event, Organization, Inventory, MembersInOrganization, User, EventOrganizators


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email')


class MembersInOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembersInOrganization
        fields = ('user', 'organization', 'role')


class EventOrganizatorsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = EventOrganizators
        fields = ('user', 'role')


class EventSerializer(serializers.ModelSerializer):
    organizators = EventOrganizatorsSerializer(many=True)

    class Meta:
        model = Event
        # m2m with trough: organizators
        fields = ('name', 'organization', 'date', 'time', 'auditorium', 'organizators', 'date_end', 'level',
                  'organizators')


class OrganizationSerializer(serializers.ModelSerializer):
    members = MembersInOrganizationSerializer(many=True)

    class Meta:
        model = Organization
        # m2m fields with trough: members
        fields = ('name', 'description', 'mission', 'motivation', 'work_trajectory', 'goal', 'members')


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('name', 'description', 'availability')


# Custom Token Serializer for logging in with email instead of username
class CustomAuthTokenSerializer(AuthTokenSerializer):
    username = None
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
