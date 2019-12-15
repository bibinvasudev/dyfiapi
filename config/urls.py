from django.conf.urls import url

from api.endpoints.config import ConfigEndpoint

urlpatterns = [
    url(r'banner_image', ConfigEndpoint.as_view({'get': 'retrieve', 'post': 'create', 'put': 'update'})),
]

config_apis = [
    url(r'banner_image', ConfigEndpoint.as_view({'get': 'retrieve', 'post': 'create', 'put': 'update'})),
]

# urlpatterns = [
#     url('/image_upload', common_config_view, name='image_upload'),
#     url('/success', success, name='success'),
#     url('/get_image', get_common_config_view, name='get_image'),
# ]
#
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)

