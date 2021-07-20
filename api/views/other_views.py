from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from api.models import EventType, EventCategory, Slide, School, Faculty
from ..serializers.other_serializers import EventTypeSerializer, EventCategorySerializer, SlideSerializer, \
    SchoolSerializer, FacultySerializer


class EventTypeViewSet(viewsets.ModelViewSet):
    """
    Тип мероприятия (Пердставление)
    """
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer

    def get_permissions(self):
        """
        Права доступа
        """
        if self.action in ['create','update', 'partial_update', 'destroy']:
            permission_classes = (IsAdminUser,)
        else:
            permission_classes = (AllowAny,)

        return [permission() for permission in permission_classes]


class EventCategoryViewSet(viewsets.ModelViewSet):
    """
    Категория мероприятия (Пердставление)
    """
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer

    def get_permissions(self):
        """
        Права доступа
        """
        if self.action in ['create','update', 'partial_update', 'destroy']:
            permission_classes = (IsAdminUser,)
        else:
            permission_classes = (AllowAny,)

        return [permission() for permission in permission_classes]


class SlideViewSet(viewsets.ModelViewSet):
    """
    Слайд (Пердставление)
    """
    queryset = Slide.objects.all()
    serializer_class = SlideSerializer

    def get_permissions(self):
        """
        Права доступа
        """
        if self.action in ['create','update', 'partial_update', 'destroy']:
            permission_classes = (IsAdminUser,)
        else:
            permission_classes = (AllowAny,)

        return [permission() for permission in permission_classes]


class SchoolViewSet(viewsets.ModelViewSet):
    """
    Школа (Пердставление)
    """
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    def get_permissions(self):
        """
        Права доступа
        """
        if self.action in ['create','update', 'partial_update', 'destroy']:
            permission_classes = (IsAdminUser,)
        else:
            permission_classes = (AllowAny,)

        return [permission() for permission in permission_classes]


class FacultyViewSet(viewsets.ModelViewSet):
    """
    Факультет (Пердставление)
    """
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer

    def get_permissions(self):
        """
        Права доступа
        """
        if self.action in ['create','update', 'partial_update', 'destroy']:
            permission_classes = (IsAdminUser,)
        else:
            permission_classes = (AllowAny,)

        return [permission() for permission in permission_classes]
