from django.conf.urls import url
from rest_framework_mongoengine import routers
from api.endpoints.members import MemberEndpoint, ExportDataEndpoint, MembersViewSet
from .views import MembersListView, MemberView, MemberSearchView


urlpatterns = [

    # url('', MembersListView.as_view(), name='members'),
    url('/search', MemberSearchView.as_view(), name='search_member'),
    url('/add', MemberView.as_view(), name='add_member'),
    url('/create', MemberView.as_view(), name='create_member'),
    url('/edit/(?P<member_id>\w+)', MemberView.as_view(), name='view_member'),
    url('/load_groups', MemberView.load_groups, name='load_groups'),

    url(r'^/export_data$', ExportDataEndpoint.as_view({'get': 'get_members_details'})),
    url(r'^/me$', MemberEndpoint.as_view({'get': 'get_my_profile', 'put': 'update_my_profile'})),
    url(r'^/me/image$', MemberEndpoint.as_view({'get': 'get_my_profile_image', 'put': 'update_my_profile_image'})),
    url(r'^/(?P<member_id>\w+)/group/add$', MemberEndpoint.as_view({'put': 'add_group'})),
    url(r'^/(?P<member_id>\w+)/group/remove$', MemberEndpoint.as_view({'put': 'remove_group'})),
    url(r'^/(?P<member_id>\w+)$', MemberEndpoint.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'delete'})),
    url(r'', MemberEndpoint.as_view({'post': 'create', 'get': 'list'})),

]

members_router = routers.DefaultRouter(trailing_slash=False)
members_router.register(r'', MembersViewSet, base_name='member')

member_apis = [
    url(r'^/export_data$', ExportDataEndpoint.as_view({'get': 'get_members_details'})),
    url(r'^/me$', MemberEndpoint.as_view({'get': 'get_my_profile', 'put': 'update_my_profile'})),
    url(r'^/me/image$', MemberEndpoint.as_view({'get': 'get_my_profile_image', 'put': 'update_my_profile_image'})),
    url(r'^/(?P<member_id>\w+)/group/add$', MemberEndpoint.as_view({'put': 'add_group'})),
    url(r'^/(?P<member_id>\w+)/group/remove$', MemberEndpoint.as_view({'put': 'remove_group'})),
    url(r'^/(?P<member_id>\w+)$', MemberEndpoint.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'delete'})),
    url(r'', MemberEndpoint.as_view({'post': 'create', 'get': 'list'}))
]


