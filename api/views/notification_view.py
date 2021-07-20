from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from api.models import Notification
from api.permissons import IsOwnerOrAdmin
from ..serializers.notification_serializer import NotificationAdminSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """
    Уведомления (Пердставление)
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationAdminSerializer

    def filter_queryset(self, queryset):
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
        if self.action in ['create']:
            permission_classes = (IsAdminUser,)
        else:
            permission_classes = (IsOwnerOrAdmin,)

        return [permission() for permission in permission_classes]


