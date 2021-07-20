from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from api.models import EventOrganizers
from api.permissons import IsLeaderOrAdmin
from ..serializers.event_organizers_serializer import EventOrganizersAdminSerializer, EventOrganizersSerializer


class EventOrganizersViewSet(viewsets.ModelViewSet):
    """
    Организаторы мероприятия (Пердставление)
    """
    queryset = EventOrganizers.objects.all()

    def get_permissions(self):
        """
        Права доступа
        """
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            permission_classes = (IsLeaderOrAdmin,)
        else:
            permission_classes = (AllowAny,)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Класс сериализатора
        """
        if self.request.user.is_staff:
            serializer_class = EventOrganizersAdminSerializer
        else:
            serializer_class = EventOrganizersSerializer

        return serializer_class
