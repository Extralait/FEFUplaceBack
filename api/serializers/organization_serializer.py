from rest_framework import serializers

from api.models import MembersInOrganization, Organization
from api.serializers.members_in_organization_serializer import MembersInOrganizationDeapSerializer


class OrganizationAdminSerializer(serializers.ModelSerializer):
    """
    Организация для администратора (Сериализатор)
    """
    members = MembersInOrganizationDeapSerializer(
        many=True, read_only=True,source='membersinorganization_set')

    def _user(self):
        """
        Получение пользователя
        """
        user = self.context['request'].user
        return user

    class Meta:
        model = Organization
        fields = '__all__'
        read_only_fields = ('id','created_at','updated_at','members')


class OrganizationSerializer(OrganizationAdminSerializer):
    """
    Организация для пользователя (Сериализатор)
    """
    status = serializers.CharField(read_only=True)

    def create(self, validated_data):
        """
        Создание организации
        """
        user = self._user()
        organization = Organization.objects.create(**validated_data)
        MembersInOrganization.objects.create(
            organization=organization,
            user_id=user.id,
            role='leader'
        )
        return organization
