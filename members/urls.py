from django.conf.urls import url
from rest_framework_mongoengine import routers
from api.endpoints.members import MemberEndpoint, ExportDataEndpoint, MembersViewSet

urlpatterns = [
    url(r'^/export_data$', ExportDataEndpoint.as_view({'get': 'get_members_details'})),
    url(r'^/me$', MemberEndpoint.as_view({'get': 'get_my_profile', 'put': 'update_my_profile'})),
    url(r'^/(?P<member_id>\w+)$', MemberEndpoint.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'delete'})),
    url(r'', MemberEndpoint.as_view({'post': 'create', 'get': 'list'}))
]

members_router = routers.DefaultRouter(trailing_slash=False)
members_router.register(r'', MembersViewSet, base_name='members')
