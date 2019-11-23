from django.conf.urls import url

from api.endpoints.groups import GroupEndpoint

urlpatterns = [
    url(r'^/(?P<group_id>\w+)/add_admin$', GroupEndpoint.as_view({'put': 'add_admin'})),
    url(r'^/(?P<group_id>\w+)/remove_admin$', GroupEndpoint.as_view({'put': 'remove_admin'})),
    url(r'^/(?P<group_id>\w+)$', GroupEndpoint.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'delete',})),
    url(r'/my_groups', GroupEndpoint.as_view({'get': 'get_my_groups'})),
    url(r'', GroupEndpoint.as_view({'post': 'create', 'get': 'list'}))
]
