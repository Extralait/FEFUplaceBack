from rest_framework import serializers

from api.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Пользователь (Сериализатор)
    """
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'image', 'name','surname',
                  'fathers_name', 'education_level','school',
                  'faculty', 'education_year','email_notification',
                  'phone', 'social_1', 'social_2', 'social_3')




