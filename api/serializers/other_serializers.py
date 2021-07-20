from rest_framework import serializers

from api.models import EventType, EventCategory, Slide, Faculty, School


class EventTypeSerializer(serializers.ModelSerializer):
    """
    Тип мероприятия (Сериализатор)
    """
    class Meta:
        model = EventType
        fields = '__all__'
        read_only_fields = ('id',)


class EventCategorySerializer(serializers.ModelSerializer):
    """
    Категория мероприятия (Сериализатор)
    """
    class Meta:
        model = EventCategory
        fields = '__all__'
        read_only_fields = ('id',)


class SlideSerializer(serializers.ModelSerializer):
    """
    Слайд (Сериализатор)
    """
    class Meta:
        model = Slide
        fields = '__all__'
        read_only_fields = ('id',)


class SchoolSerializer(serializers.ModelSerializer):
    """
    Школа (Сериализатор)
    """
    class Meta:
        model = School
        fields = '__all__'
        read_only_fields = ('id',)


class FacultySerializer(serializers.ModelSerializer):
    """
    Факультет (Сериализатор)
    """
    class Meta:
        model = Faculty
        fields = '__all__'
        read_only_fields = ('id',)

