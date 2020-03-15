from django.conf.urls import url
from rest_framework import routers

from apps.blog import api_views

urlpatterns = [
    url(r'^about$', api_views.AboutViews.as_view(), name='about'),
]
