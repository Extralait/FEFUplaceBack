from django.contrib import admin
from .models import Event, Organization, Inventory

admin.site.register(Event)
admin.site.register(Organization)
admin.site.register(Inventory)
