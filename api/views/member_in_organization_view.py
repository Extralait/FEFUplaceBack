from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.models import MembersInOrganization
from api.permissons import IsOwnerOrAdmin, IsLeaderOrAdmin
from ..serializers.members_in_organization_serializer import MembersInOrganizationAdminSerializer, \
    MembersInOrganizationForUserSerializer, MembersInOrganizationForOrganizationSerializer


class MembersInOrganizationForUserViewSet(viewsets.ModelViewSet):
    """
    Члены организаций для пользователей (Пердставление)
    """
    queryset = MembersInOrganization.objects.all()

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
        if self.action in ['create']:
            permission_classes = (IsAuthenticated,)
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = (IsOwnerOrAdmin,)
        else:
            permission_classes = (AllowAny,)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Класс сериализатора
        """
        if self.request.user.is_staff:
            serializer_class = MembersInOrganizationAdminSerializer
        else:
            serializer_class = MembersInOrganizationForUserSerializer

        return serializer_class


class MembersInOrganizationForOrganizationViewSet(viewsets.ModelViewSet):
    """
    Члены организаций для организаций (Пердставление)
    """
    queryset = MembersInOrganization.objects.all()

    def get_permissions(self):
        """
        Права доступа
        """
        if self.action in ['create','update', 'partial_update', 'destroy']:
            permission_classes = (IsLeaderOrAdmin,)
        else:
            permission_classes = (AllowAny,)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Класс сериализатора
        """
        if self.request.user.is_staff:
            serializer_class = MembersInOrganizationAdminSerializer
        else:
            serializer_class = MembersInOrganizationForOrganizationSerializer

        return serializer_class
