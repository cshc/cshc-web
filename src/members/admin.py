""" Configuration of Members models for the admin interface.
"""

from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from image_cropping import ImageCroppingMixin
from members.models import Member, CommitteeMembership, CommitteePosition, SquadMembership


class SquadMembershipInline(admin.TabularInline):
    """ Allows squad membership to be edited from the admin page of the member model."""
    model = SquadMembership
    extra = 0


@admin.register(Member)
class MemberAdmin(ImageCroppingMixin, admin.ModelAdmin):
    """ Admin interface definition for the Member model."""
    model = Member
    inlines = (SquadMembershipInline,)
    search_fields = ('first_name', 'known_as', 'last_name')
    list_filter = ('is_current', 'gender', 'pref_position',
                   'shirt_number', 'is_umpire', 'is_coach')
    list_display = ('full_name_with_option', 'user', 'gender', 'pref_position',
                    'shirt_number', 'is_current', 'is_umpire', 'is_coach')
    fieldsets = [
        ('Personal', {'fields': ['user', 'first_name', 'known_as', 'last_name',
                                 'gender', 'profile_pic', 'profile_pic_cropping']}),
        ('Playing', {'fields': ['is_current', 'shirt_number',
                                'pref_position', 'is_umpire', 'is_coach']}),
        ('Contact', {'fields': ['email', 'phone', 'addr_street',
                                'addr_line2', 'addr_town', 'addr_postcode', 'addr_position']}),
        ('Medical', {'fields': ['dob', 'emergency_contact',
                                'emergency_relationship', 'emergency_phone', 'medical_notes']}),
    ]

    class Media:
        css = {
            'all': ('css/admin.css',)
        }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            User = get_user_model()

            class UserChoiceField(forms.ModelChoiceField):
                def label_from_instance(self, obj):
                    full_name = f"{obj.first_name} {obj.last_name}".strip()
                    email = (obj.email or "").strip()

                    if full_name and email:
                        return f"{full_name} ({email})"
                    if full_name:
                        return full_name
                    if email:
                        return email
                    return str(obj)

            kwargs["queryset"] = User.objects.all().order_by("first_name", "last_name", "email")
            kwargs["form_class"] = UserChoiceField

        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == "user":
            existing = formfield.widget.attrs.get("class", "")
            formfield.widget.attrs["class"] = f"{existing} member-user-select".strip()

        return formfield

    def full_name_with_option(self, obj):
        return "{}{} {}".format(obj.first_name, " ({})".format(obj.known_as) if obj.known_as else '', obj.last_name)

    full_name_with_option.short_description = 'Name'


@admin.register(SquadMembership)
class SquadMembershipAdmin(admin.ModelAdmin):
    """ Admin interface definition for the SquadMembership model."""
    model = SquadMembership
    search_fields = ('member__first_name',
                     'member__known_as', 'member__last_name')
    list_filter = ('member', 'team', 'season')
    list_display = ('__str__', 'member', 'team', 'season')


@admin.register(CommitteePosition)
class CommitteePositionAdmin(admin.ModelAdmin):
    """ Admin interface definition for the CommitteePosition model."""
    model = CommitteePosition
    search_fields = ('name',)
    list_filter = ('name', 'gender')
    list_display = ('__str__', 'name', 'gender')


@admin.register(CommitteeMembership)
class CommitteeMembershipAdmin(admin.ModelAdmin):
    """ Admin interface definition for the CommitteeMembership model."""
    model = CommitteeMembership
    search_fields = ('member__first_name',
                     'member__known_as', 'member__last_name')
    list_filter = ('member', 'position', 'season')
    list_display = ('__str__', 'member', 'position', 'season')
