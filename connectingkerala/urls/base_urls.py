"""connectingkerala URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
from connectingkerala.views import LoginViewSet, base_redirect
from levels.urls import level_apis
from members.urls import member_apis
from groups.urls import group_apis
from config.urls import config_apis
from .web import urlpatterns as web_urls

urlpatterns = [
    url(r'^admin_login', LoginViewSet.as_view(actions={'post': 'admin_login'}), name='admin_login'),
    url(r'^login', LoginViewSet.as_view(actions={'post': 'login'}), name='login'),
    url(r'^levels', include(level_apis, namespace='levels')),
    url(r'^groups', include(group_apis, namespace='groups')),
    url(r'^members', include(member_apis, namespace='members')),
    url(r'^config', include(config_apis, namespace='config')),
    url(r'^web/', include(web_urls, namespace='web')),
    url('', base_redirect, name='base_redirect'),
]
