from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from .views.auth_view import UserActivationView, PasswordResetConfirmView
from .views.event_guests_view import EventGuestsViewSet
from .views.event_organizers_view import EventOrganizersViewSet
from .views.event_view import EventViewSet
from .views.member_in_organization_view import MembersInOrganizationForUserViewSet, \
    MembersInOrganizationForOrganizationViewSet
from .views.notification_view import NotificationViewSet
from .views.organization_view import OrganizationViewSet
from .views.other_views import EventCategoryViewSet, EventTypeViewSet, SlideViewSet, SchoolViewSet, FacultyViewSet

router = routers.DefaultRouter()
router.register(r'event-categories', EventCategoryViewSet)
router.register(r'event-types', EventTypeViewSet)
router.register(r'events', EventViewSet)
router.register(r'event-organizers', EventOrganizersViewSet)
router.register(r'event-guests', EventGuestsViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'organization-members-for-users', MembersInOrganizationForUserViewSet)
router.register(r'organization-members-for-organizations', MembersInOrganizationForOrganizationViewSet)
router.register(r'notification', NotificationViewSet)
router.register(r'slides', SlideViewSet)
router.register(r'schools', SchoolViewSet)
router.register(r'faculties', FacultyViewSet)

urlpatterns = [
    # DRF router
    path('', include(router.urls)),
    # djoser auth urls
    url(r'^auth/', include('djoser.urls')),
    # djoser auth jwt urls
    url(r'^auth/', include('djoser.urls.jwt')),
    # Активация профиля пользователя
    path('activate/<str:uid>/<str:token>/', UserActivationView.as_view()),
    # Смена пароля пользователя
    path('password/reset/confirm/<str:uid>/<str:token>/', PasswordResetConfirmView.as_view()),
    # Логин GUI DRF
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]