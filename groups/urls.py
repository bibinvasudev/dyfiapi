from django.conf.urls import url

from api.endpoints.groups import GroupEndpoint

urlpatterns = [
    url(r'^/(?P<group_id>\w+)$', GroupEndpoint.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'delete'})),
    url(r'', GroupEndpoint.as_view({'post': 'create', 'get': 'list'}))
]
