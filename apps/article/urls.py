from django.conf.urls import url
from rest_framework import routers

from apps.article import api_views

urlpatterns = [
    # 获取文章详细信息
    url(r'^detail/(?P<pk>\d+)$', api_views.ArticleDetail.as_view(), name='detail'),
    # 获取文正分类信息
    url(r'^categories/(?P<pk>\d+)$', api_views.Categories.as_view({'get': 'categories'}), name='categories'),
    # 获取指定分类的文章
    url(r'^category/articles/(?P<name>\S+)$', api_views.CategoryArticles.as_view({'get': 'categoryArticles'}),
        name='category_articles'),
    # 点赞
    url(r'^love/(?P<pk>\d+)$', api_views.Love.as_view({'put': 'love'}), name='love'),

]
router = routers.DefaultRouter()
# 获取文章列表
router.register(r'list', api_views.ArticleListViews, basename='article_list')
router.register(r'hot', api_views.ArticleHotViews, basename='article_hot')
urlpatterns += router.urls
