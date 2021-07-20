from rest_framework import serializers
from rest_framework.exceptions import APIException

from api.models import EventOrganizers, MembersInOrganization


class EventOrganizersDeapSerializer(serializers.ModelSerializer):
    """
    Организаторы мероприятий для сериализатиора мероприятий (Сериализатор)
    """
    class Meta:
        model = MembersInOrganization
        fields = ('user', 'role')


class EventOrganizersAdminSerializer(serializers.ModelSerializer):
    """
    Организаторы мероприятия для администратора (Сериализатор)
    """
    def _user(self):
        """
        Получение пользователя
        """
        user = self.context['request'].user
        return user

    def _leader_ids(self):
        """
        Получение id организаций и мероприятий лидера
        """
        leader_events = []
        leader_orgs = []

        event_rows = EventOrganizers.objects.all().filter(user_id=self._user().id)
        orgs_rows = MembersInOrganization.objects.all().filter(user_id=self._user().id)
        for row in event_rows:
            if row.role in ['leader']:
                leader_events.append(row.event_id)
        for row in orgs_rows:
            if row.role in ['leader', 'admin']:
                leader_orgs.append(row.organization_id)
        return leader_events, leader_orgs

    class Meta:
        model = EventOrganizers
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class EventOrganizersSerializer(EventOrganizersAdminSerializer):
    """
    Организаторы мероприятия для пользователей (Сериализатор)
    """
    def create(self, validated_data):
        """
        Создание организатора мероприятия
        """
        if (validated_data['event'].id not in self._leader_ids()[0] and
                validated_data['event'].organization.id not in self._leader_ids()[1]):
            raise APIException("Вы не являетесь руководителем этого мероприятия")
        event_organizer = EventOrganizers.objects.create(**validated_data)
        return event_organizer

    def update(self, instance, validated_data):
        """
        Обновление организатора мероприятия
        """
        if (validated_data['event'].id not in self._leader_ids()[0] and
                validated_data['event'].organization.id not in self._leader_ids()[1]):

            raise APIException("Вы не являетесь руководителем этого мероприятия")
        instance.role = validated_data.get('role', instance.role)
        instance.event = validated_data.get('event', instance.event)
        instance.user = validated_data.get('user', instance.user)
        instance.save()
        return instance
