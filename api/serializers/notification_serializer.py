from rest_framework import serializers

from api.models import Notification


class NotificationAdminSerializer(serializers.ModelSerializer):
    """
    Уведомление для администратора (Сериализатор)
    """
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('id','created_at','updated_at')


class NotificationSerializer(serializers.ModelSerializer):
    """
    Уведомление для пользователей (Сериализатор)
    """
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('user_id','message','link','id','created_at','updated_at')
