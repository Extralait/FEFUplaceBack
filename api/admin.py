from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import Event, Organization, Inventory, User

admin.site.register(Event)
admin.site.register(Organization)
admin.site.register(Inventory)


# Custom User admin with no username field
@admin.register(User)
class UserAdmin(DjangoUserAdmin):

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'full_name')
    search_fields = ('email', 'full_name', )
    ordering = ('email',)