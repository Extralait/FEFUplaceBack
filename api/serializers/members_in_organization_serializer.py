from sqlite3 import IntegrityError

from rest_framework import serializers
from rest_framework.exceptions import APIException

from api.models import MembersInOrganization


class MembersInOrganizationDeapSerializer(serializers.ModelSerializer):
    """
    Члены организации для сериализатора организации (Сериализатор)
    """
    class Meta:
        model = MembersInOrganization
        fields = ('user', 'role')


class MembersInOrganizationAdminSerializer(serializers.ModelSerializer):
    """
    Члены организации для администратора (Сериализатор)
    """
    def _user(self):
        """
        Получение пользователя
        """
        user = self.context['request'].user
        return user

    def _leader_organisations(self):
        """
        Получение id организаций лидера
        """
        leader_organizations = []
        member_rows = MembersInOrganization.objects.all().filter(user_id=self._user().id)
        for row in member_rows:
            if row.role in ['leader', 'admin']:
                leader_organizations.append(row.organization_id)
        return leader_organizations

    class Meta:
        model = MembersInOrganization
        fields = ('id','organization','user',
                  'role','organization_confirm',
                  'user_confirm','user_confirm',
                  'created_at', 'updated_at')
        read_only_fields = ('id','created_at', 'updated_at')


class MembersInOrganizationForOrganizationSerializer(MembersInOrganizationAdminSerializer):
    """
    Члены организации для организаций (Сериализатор)
    """
    user_confirm = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        """
        Создания члена организации
        """
        if validated_data['organization'].id not in self._leader_organisations():
            raise APIException("Вы не являетесь руководителем этой организации")
        else:
            member_in_organization = (MembersInOrganization.objects.create(**validated_data))
            return member_in_organization

    def update(self, instance, validated_data):
        """
        Обновление члена организации
        """
        instance.role = validated_data.get('role', instance.role)
        instance.organization_confirm = validated_data.get('organization_confirm',
                                                           instance.organization_confirm)
        instance.save()
        return instance


class MembersInOrganizationForUserSerializer(MembersInOrganizationAdminSerializer):
    """
    Члены организации для пользователей (Сериализатор)
    """
    organization_confirm = serializers.BooleanField(read_only=True)
    role = serializers.CharField(read_only=True)

    def create(self, validated_data):
        """
        Создание члена организации
        """
        member_in_organization = (MembersInOrganization.objects.create(
            role='member',
            user_id=self._user().id,
            **validated_data))
        return member_in_organization

    def update(self, instance, validated_data):
        """
        Обновление члена организации
        """
        instance.user_confirm = validated_data.get('user_confirm',
                                                   instance.user_confirm)
        instance.save()
        return instance

    class Meta(MembersInOrganizationAdminSerializer.Meta):
        read_only_fields = ('id','created_at', 'updated_at','user')

