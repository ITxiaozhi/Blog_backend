from django.conf.urls import url
from rest_framework import routers

from apps.blog import api_views

urlpatterns = [
    url(r'^about$', api_views.AboutViews.as_view(), name='about'),
]
router = routers.DefaultRouter()
# 添加留言
router.register(r'message', api_views.MessageViews, basename='message')
urlpatterns += router.urls
