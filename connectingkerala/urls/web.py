from django.conf.urls import url
from django.conf.urls import include

from connectingkerala.views import LoginView, home

urlpatterns = [
    url(r'^home', home, name='home'),
    url(r'^levels', include('levels.urls', namespace='levels')),
    url(r'^groups', include('groups.urls', namespace='groups')),
    url(r'^members', include('members.urls', namespace='members')),
    url(r'^config', include('config.urls', namespace='config')),
    url(r'^login', LoginView.as_view(), name='login'),
]
