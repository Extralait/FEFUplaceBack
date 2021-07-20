from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission

from api.models import Organization, MembersInOrganization, EventOrganizers, Event




class IsOwnerOrAdmin(BasePermission):
    """
    Владелец или администратор
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Проверка прав доступа
        """
        user_email = obj.user.email
        is_self = user_email == request.user.email
        is_admin = bool(request.user and request.user.is_staff)
        return is_self or is_admin


class IsLeaderOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if type(user) == AnonymousUser:
            return False
        if type(obj) in [Organization, MembersInOrganization]:
            if type(obj) == Organization:
                obj_id = obj.id
            else:
                obj_id = obj.organization_id
            leader_table = (MembersInOrganization.objects.all()
                                      .filter(user=user)
                                      .filter(organization_id=obj_id))
        else:
            if type(obj) == Event:
                event_id = obj.id
                org_id = obj.organization.id
            else:
                event_id = obj.id
                org_id = obj.event.organization.id
            leader_table_event = (EventOrganizers.objects.all()
                                      .filter(user=user)
                                      .filter(event_id=event_id))
            leader_table_org =(MembersInOrganization.objects.all()
                                      .filter(user=user)
                                      .filter(organization_id=org_id))
            leader_table = leader_table_event if leader_table_event.count() else leader_table_org

        if leader_table.count() and leader_table[0].role in ['leader', 'admin']:
            is_leader = True
        else:
            is_leader = False
        is_admin = bool(request.user and request.user.is_staff)

        return is_leader or is_admin


class IsOrganizationMemberOrAdmin(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if type(user) == AnonymousUser:
            return False

        user_intermediate_rows = MembersInOrganization.objects.all().filter(user=request.user)

        if user_intermediate_rows:
            is_member = True
        else:
            is_member = False

        is_admin = bool(request.user and request.user.is_staff)

        return is_member or is_admin
