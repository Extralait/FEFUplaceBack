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
        ('Personal info', {'fields': ('full_name',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'full_name')
    search_fields = ('email', 'full_name',)
    ordering = ('email',)
