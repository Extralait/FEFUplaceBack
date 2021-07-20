from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from api.models import EventGuests
from api.permissons import IsOwnerOrAdmin
from ..serializers.event_guests_serializer import EventGuestsAdminSerializer, EventGuestsSerializer


class EventGuestsViewSet(viewsets.ModelViewSet):
    """
    Посетители мероприятия (Пердставление)
    """
    queryset = EventGuests.objects.all()

    def filter_queryset(self, queryset):
        """
        Фильтрация набора данных
        """
        user = self.request.user
        if user.is_staff:
            queryset = queryset
        else:
            queryset = queryset.filter(user=user)

        return queryset

    def get_permissions(self):
        """
        Права доступа
        """
        if self.action in ['destroy']:
            permission_classes = (IsOwnerOrAdmin,)
        elif self.action in ['created']:
            permission_classes = (IsAuthenticated,)
        elif self.action in ['update', 'partial_update']:
            permission_classes = (IsAdminUser,)
        else:
            permission_classes = (AllowAny,)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Класс сериализатора
        """
        if self.request.user.is_staff:
            serializer_class = EventGuestsAdminSerializer
        else:
            serializer_class = EventGuestsSerializer

        return serializer_class