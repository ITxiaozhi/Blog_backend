"""Blog_backend URL Configuration

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
from extra_apps import xadmin
from django.conf.urls import url, include
from django.contrib import admin

from apps.article.views import upload

xadmin.autodiscover()
from xadmin.plugins import xversion

xversion.register_models()
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'mdeditor/uploads/', upload),
    url(r'mdeditor/', include('mdeditor.urls')),
    url(r'blog/', include('apps.blog.urls', namespace='blog')),
    url(r'article/', include('apps.article.urls', namespace='article')),
]
