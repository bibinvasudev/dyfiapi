from django.conf.urls import url

from api.endpoints.members import MemberEndpoint, get_members_details

urlpatterns = [
    url(r'^/export_data$', get_members_details, name='export_data'),
    url(r'^/me$', MemberEndpoint.as_view({'get': 'get_my_profile', 'put': 'update_my_profile'})),
    url(r'^/(?P<member_id>\w+)$', MemberEndpoint.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'delete'})),
    url(r'', MemberEndpoint.as_view({'post': 'create', 'get': 'list'}))
]
