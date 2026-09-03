""" Configuration of Members models for the admin interface.
"""

from django.contrib import admin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from image_cropping import ImageCroppingMixin
from core.models import ClubInfo, Gender
from members.models import Member, CommitteeMembership, CommitteePosition, SquadMembership, ShirtNumberOverview


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
                   'is_umpire', 'is_coach')
    list_display = ('full_name_with_option', 'user', 'gender',
                    'pref_position', 'is_current', 'is_umpire', 'is_coach')
    fieldsets = [
        ('Personal', {'fields': ['user', 'first_name', 'known_as', 'last_name',
                                 'gender', 'profile_pic', 'profile_pic_cropping']}),
        ('Playing', {'fields': ['is_current', 'shirt_number', 'shirt_number_hold_until',
                                'pref_position', 'is_umpire', 'is_coach']}),
        ('Contact', {'fields': ['email', 'phone', 'addr_street',
                                'addr_line2', 'addr_town', 'addr_postcode', 'addr_position']}),
        ('Medical', {'fields': ['dob', 'emergency_contact',
                                'emergency_relationship', 'emergency_phone', 'medical_notes']}),
    ]

    def full_name_with_option(self, obj):
        return "{}{} {}".format(obj.first_name, " ({})".format(obj.known_as) if obj.known_as else '', obj.last_name)

    full_name_with_option.short_description = 'Name'


@admin.register(ShirtNumberOverview)
class ShirtNumberOverviewAdmin(admin.ModelAdmin):
    """ Read-only admin view listing shirt numbers 1..ShirtNumMax per gender,
        showing which member(s) currently hold each number. """

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        # Change permission gates visibility in the admin index. We need True
        # for the entry to appear, but the changelist itself is overridden
        # below so no editing is exposed.
        return request.user.is_staff

    #: (gender value, column header) pairs, left-to-right.
    gender_columns = (
        (Gender.Male, "Men's"),
        (Gender.Female, "Ladies'"),
    )

    #: Rows (numbers) per page - matches Django admin default list_per_page.
    list_per_page = 100

    def changelist_view(self, request, extra_context=None):
        max_shirt_number_obj, _ = ClubInfo.objects.get_or_create(
            key='ShirtNumMax', defaults={'value': '199'})
        max_shirt_number = int(max_shirt_number_obj.value)

        search_query = (request.GET.get('q') or '').strip()

        buckets_by_gender = {}
        for gender_value, _label in self.gender_columns:
            active = Member.objects._get_members_with_active_shirt_numbers_queryset(gender_value).only(
                'pk', 'first_name', 'known_as', 'last_name', 'shirt_number')
            buckets = {}
            for member in active:
                raw = (member.shirt_number or '').strip()
                if not raw:
                    continue
                try:
                    n = int(raw)
                except ValueError:
                    continue
                if 1 <= n <= max_shirt_number:
                    buckets.setdefault(n, []).append(member)
            buckets_by_gender[gender_value] = buckets

        all_rows = [
            (n, [buckets_by_gender[g].get(n, []) for g, _ in self.gender_columns])
            for n in range(1, max_shirt_number + 1)
        ]

        if search_query:
            needle = search_query.lower()
            def matches(cells):
                for members in cells:
                    for member in members:
                        if needle in member.full_name().lower():
                            return True
                return False

            if needle.isdigit():
                target = int(needle)
                filtered_rows = [(n, cells) for n, cells in all_rows if n == target or matches(cells)]
            else:
                filtered_rows = [(n, cells) for n, cells in all_rows if matches(cells)]
        else:
            filtered_rows = all_rows

        paginator = Paginator(filtered_rows, self.list_per_page)
        page_number = request.GET.get('p') or 1
        try:
            page = paginator.page(page_number)
        except (PageNotAnInteger, EmptyPage):
            page = paginator.page(1)

        context = dict(
            self.admin_site.each_context(request),
            title='Shirt numbers',
            opts=self.model._meta,
            column_headers=[label for _, label in self.gender_columns],
            page=page,
            paginator=paginator,
            search_query=search_query,
            result_count=len(filtered_rows),
            full_result_count=len(all_rows),
        )
        return render(request, 'admin/members/shirtnumberoverview/grid.html', context)


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
