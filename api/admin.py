from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import Event, Organization, User, EventOrganizers, MembersInOrganization, Notification, EventCategory, \
    Slide, EventType, EventGuests, School, Faculty


class OrganizersInline(admin.TabularInline):
    model = EventOrganizers
    extra = 1


class MembersInline(admin.TabularInline):
    model = MembersInOrganization
    extra = 1


class EventAdmin(admin.ModelAdmin):
    inlines = (OrganizersInline,)


class OrganizationAdmin(admin.ModelAdmin):
    inlines = (MembersInline,)


admin.site.register(Event, EventAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(EventCategory)
admin.site.register(EventType)
admin.site.register(Slide)
admin.site.register(School)


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('school', 'name')


@admin.register(EventOrganizers)
class EventOrganizersAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'role')


@admin.register(EventGuests)
class EventGuestsAdmin(admin.ModelAdmin):
    list_display = ('user', 'event')


@admin.register(MembersInOrganization)
class MembersInOrganizationAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'role', 'organization_confirm','user_confirm')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message')


# Custom User admin with no username field
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'surname', 'fathers_name','education_level',
                                      'school','faculty','education_year',)}),
        ('Personal contacts', {'fields': ('phone', 'social_1', 'social_2','social_3')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser','email_notification'),
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
