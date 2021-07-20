from rest_framework import serializers

from api.models import EventGuests


class EventGuestsAdminSerializer(serializers.ModelSerializer):
    """
    Посетители мероприятия для администратора (Сериализатор)
    """
    def _user(self):
        """
        Получение пользователя
        """
        user = self.context['request'].user
        return user

    class Meta:
        model = EventGuests
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class EventGuestsSerializer(EventGuestsAdminSerializer):
    """
    Посетилеи мероприятия для пользователя (Сериализатор)
    """
    def create(self, validated_data):
        """
        Создание посетителя мероприятия
        """
        user = self._user()
        event_guests = EventGuests.objects.create(user_id=user.id, **validated_data)
        return event_guests

    class Meta(EventGuestsAdminSerializer.Meta):
        read_only_fields = ('id', 'created_at', 'updated_at','user')
