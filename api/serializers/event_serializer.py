from rest_framework import serializers

from api.models import EventOrganizers, Event
from api.serializers.event_guests_serializer import EventGuestsSerializer
from api.serializers.event_organizers_serializer import EventOrganizersDeapSerializer


class EventAdminSerializer(serializers.ModelSerializer):
    """
    Мероприятие для администратора (Сериализатор)
    """
    organizers = EventOrganizersDeapSerializer(many=True, read_only=True,
                                           source='eventorganizers_set')
    guests = EventGuestsSerializer(many=True, read_only=True,
                                   source='eventguests_set')

    def _user(self):
        """
        Получение пользователя
        """
        user = self.context['request'].user
        return user

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'organizers', 'guests')


class EventSerializer(EventAdminSerializer):
    """
    Мероприятие для пользователей (Сериализатор)
    """
    status = serializers.CharField(read_only=True)

    def create(self, validated_data):
        """
        Создание мероприятия
        """
        user = self._user()
        event_categories = validated_data.pop('event_category', None)
        event_types = validated_data.pop('event_type', None)
        event = Event.objects.create(**validated_data)
        for event_category in event_categories:
            event.event_category.add(event_category)
        for event_type in event_types:
            event.event_type.add(event_type)

        EventOrganizers.objects.create(
            user_id=user.id,
            role='leader',
            event=event)
        return event
