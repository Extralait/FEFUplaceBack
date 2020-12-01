from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import EventViewSet, OrganizationViewSet, InventoryViewSet, CustomAuthToken

router = routers.DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'inventory', InventoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomAuthToken.as_view(), name='token'),
]