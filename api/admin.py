from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import Event, Organization, Inventory, User, EventOrganizators, MembersInOrganization


class OrganizatorsInline(admin.TabularInline):
    model = EventOrganizators
    extra = 1


class MembersInline(admin.TabularInline):
    model = MembersInOrganization
    extra = 1


class EventAdmin(admin.ModelAdmin):
    inlines = (OrganizatorsInline,)


class OrganizationAdmin(admin.ModelAdmin):
    inlines = (MembersInline,)


admin.site.register(Event, EventAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Inventory)


# Custom User admin with no username field
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'surname', 'fathers_name')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'name', 'surname', 'fathers_name')
    search_fields = ('email', 'name',)
    ordering = ('email',)
