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
    url(r'^(?P<pk>\d+)/$',
        views.MemberDetailView.as_view(),
        name="member_detail"
        ),
]
