from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.utils.translation import gettext_lazy as _

from .models import Event, Organization, Inventory, MembersInOrganization, User, EventOrganizators


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'image', 'name',
                  'surname', 'fathers_name', 'education_level',
                  'phone', 'social_1', 'social_2',
                  'social_3')


class MembersInOrganizationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = MembersInOrganization
        fields = ('user', 'role')


class EventOrganizatorsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    grant = serializers.IntegerField(read_only=True)

    role_multipliers = {
        'leader': '10.0',
        'manager': '6.0',
        'executor': '4.0',
        'volonteer': '2.0',
    }
    level_multipliers = {
        'international': '1.2',
        'country': '1.2',
        'regional': '1.2',
        'university': '1.8',
    }
    duration_multipliers = {
        '1-3': '1.1',
        '4-21': '1.4',
        '22-70': '1.7',
        '<71': '2.0'
    }

    class Meta:
        model = EventOrganizators
        fields = ('user', 'role', 'grant')

    def create(self, validated_data):
        obj = self.get_object()
        role = validated_data['role']
        level = obj.event.level
        validated_data['grant'] = self.role_multipliers[role] \
                                  * self.level_multipliers[level]
        return super(EventOrganizatorsSerializer, self).create(validated_data)


class EventSerializer(serializers.ModelSerializer):
    organizators = EventOrganizatorsSerializer(many=True, required=False)

    class Meta:
        model = Event
        # m2m with trough: organizators
        fields = ('id', 'name', 'organization', 'date', 'time', 'auditorium', 'organizators', 'date_end', 'level',
                  'organizators', 'guests')

    def create(self, validated_data):
        organization = validated_data.pop('organization', None)
        organizators = validated_data.pop('organizators', None)
        guests = validated_data.pop('guests', None)
        event = Event.objects.create(**validated_data)
        if organization:
            event.organization.set(organization)
        if guests:
            event.guests.set(guests)
        if organizators:
            EventOrganizators.objects.create(event=event, **organizators)
        return event


class OrganizationSerializer(serializers.ModelSerializer):
    members = MembersInOrganizationSerializer(many=True, required=False)

    class Meta:
        model = Organization
        # m2m fields with trough: members
        fields = ('id', 'name', 'description', 'mission',
                  'motivation', 'work_trajectory', 'goal',
                  'members', 'social_network_1', 'social_network_2',
                  'phone', 'email')

    def create(self, validated_data):
        members = validated_data.pop('members', None)
        organization = Organization.objects.create(**validated_data)
        if members:
            MembersInOrganization.objects.create(organization=organization, **members)
        return organization


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
