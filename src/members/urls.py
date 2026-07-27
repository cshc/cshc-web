""" URL routing for the Member views.
"""

from django.conf.urls import url
from . import views

urlpatterns = [

    # E.g. '/members/'                  - Lists all club members. Filterable.
    url(r'^$',
        views.MemberListView.as_view(),
        name="member_list"
        ),

    # E.g. '/members/32/'               - Details of a particular member
    url(r'^(?P<pk>\d+)/.*$',            # Note the trailing '.*' is important as this URL uses react-router to manipulate the rest of this URL
        views.MemberDetailView.as_view(),
        name="member_detail"
        ),

    # New AJAX endpoints for shirt numbers
    url(r'^members/available-shirt-numbers/$', views.get_available_shirt_numbers, name='available_shirt_numbers'),
    url(r'^members/assign-shirt-number/$', views.assign_shirt_number, name='assign_shirt_number'),
]
