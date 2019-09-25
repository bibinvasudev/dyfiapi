from django.conf.urls import url

from api.endpoints.levels import LevelEndpoint

urlpatterns = [
    url(r'^/(?P<level_id>\w+)$', LevelEndpoint.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'delete'})),
    url(r'', LevelEndpoint.as_view({'post': 'create', 'get': 'list'}))
]
