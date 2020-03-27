from django.conf.urls import url
from rest_framework import routers

from apps.article import api_views

urlpatterns = [
    # 获取文章详细信息
    url(r'^detail/(?P<pk>\d+)$', api_views.ArticleDetail.as_view(), name='detail'),
    # 获取文章分类信息
    url(r'^categories/(?P<pk>\d+)$', api_views.Categories.as_view({'get': 'categories'}), name='categories'),
    # 获取指定分类的文章
    url(r'^category/(?P<name>\S+)$', api_views.CategoryArticles.as_view({'get': 'categoryArticles'}),
        name='category_articles'),
    # 获取指定日期的文章
    url(r'^archive/(?P<date>\S+)$', api_views.ArchiveArticles.as_view({'get': 'archiveArticles'}),
        name='archive_articles'),
    # 获取指定标签的文章
    url(r'^tag/(?P<tag>\S+)$', api_views.TagArticles.as_view({'get': 'tagArticles'}),
        name='tag_articles'),
    # 点赞
    url(r'^love/(?P<pk>\d+)$', api_views.Love.as_view({'put': 'love'}), name='love'),

]
router = routers.DefaultRouter()
# 获取文章列表
router.register(r'list', api_views.ArticleListViews, basename='article_list')
router.register(r'hot', api_views.ArticleHotViews, basename='article_hot')
router.register(r'archive', api_views.Archive, basename='archive')
router.register(r'tag', api_views.TagList, basename='tag_list')
router.register(r'timeline', api_views.TimelineViews, basename='timeline')
urlpatterns += router.urls
