from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from api.models import Organization
from api.permissons import IsLeaderOrAdmin
from ..serializers.organization_serializer import OrganizationAdminSerializer, OrganizationSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    Оргпнизации (Пердставление)
    """
    queryset = Organization.objects.all()

    def get_permissions(self):
        """
        Права доступа
        """
        if self.action in ['create']:
            permission_classes = (IsAuthenticated,)
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
            serializer_class = OrganizationAdminSerializer
        else:
            serializer_class = OrganizationSerializer

        return serializer_class
