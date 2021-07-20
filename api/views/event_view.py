from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from api.models import Event
from api.permissons import IsLeaderOrAdmin, IsOrganizationMemberOrAdmin
from ..serializers.event_serializer import EventAdminSerializer, EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    """
    События (Пердставление)
    """
    queryset = Event.objects.all()

    def get_permissions(self):
        """
        Права доступа
        """
        if self.action in ['create']:
            permission_classes = (IsOrganizationMemberOrAdmin,)
        elif self.action in ['destroy']:
            permission_classes = (IsAdminUser,)
        elif self.action in ['update', 'partial_update']:
            permission_classes = (IsLeaderOrAdmin,)
        else:
            permission_classes = (AllowAny,)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Класс сериализатора
        """
        if self.request.user.is_staff:
            serializer_class = EventAdminSerializer
        else:
            serializer_class = EventSerializer

        return serializer_class
