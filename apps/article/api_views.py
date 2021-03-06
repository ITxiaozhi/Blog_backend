import markdown
from django.contrib.syndication.views import Feed
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from Blog_backend import settings
from apps.article.article_serializers import ArticleListSerializer, ArticleSerializer, CategorySerializer, \
    ArchiveSerializer, TagSerializer, TimeLineSerializer
from apps.article.models import Article, Category, Tag
from apps.article.utils import PageNum


class ArticleListViews(ModelViewSet):
    """
    获取文章列表类
    """
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ('create_date',)
    pagination_class = PageNum


class ArticleDetail(APIView):
    """
    获取文正详情类
    """

    def get(self, request, pk):
        """
        获取文章
        """

        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response('404')
        # 阅读量加一
        article.views = article.views + 1
        article.save()
        # 将body转成Markdown格式
        article.body = markdown.markdown(article.body,
                                         extensions=[
                                             'markdown.extensions.extra',
                                             'markdown.extensions.codehilite',
                                             'markdown.extensions.toc',
                                         ])
        serializer = ArticleSerializer(article)

        return Response(serializer.data)


class Categories(ModelViewSet):
    """
    获取分类列表类
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def categories(self, request, pk):
        if pk == '1':
            categories = Category.objects.filter(bigcategory__name='技术杂谈')
        elif pk == '2':
            categories = Category.objects.filter(bigcategory__name='开发工具')
        else:
            return Response('参数错误')
        ser = CategorySerializer(categories, many=True)

        return Response(ser.data)


class CategoryArticles(ModelViewSet):
    """
    获取指定分类的文章列表
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = PageNum

    def categoryArticles(self, request, name):
        queryset = Article.objects.filter(category__name=name).order_by('-create_date')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ArticleHotViews(ModelViewSet):
    """
    获取热门文章列表类
    """
    queryset = Article.objects.filter().order_by('-views')[:5]
    serializer_class = ArticleListSerializer


class Love(ModelViewSet):
    """
    文章点赞功能
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def love(self, request, pk):
        article = Article.objects.filter(id=pk)[0]
        article.loves += 1
        article.save()
        ser = ArticleSerializer(article)
        return Response(ser.data)


class Archive(ModelViewSet):
    """
    获取文章归档列表
    """

    serializer_class = ArchiveSerializer

    def get_queryset(self):
        distinct_date_list = []
        articles = Article.objects.all().order_by('-create_date')
        for date in articles:
            flag = False
            date = date.create_date.strftime('%Y-%m')
            for distinct_date in distinct_date_list:
                if distinct_date['create_date'] == date:
                    flag = True
            if not flag:
                distinct_date_list.append({'create_date': date})
        return distinct_date_list


class ArchiveArticles(ModelViewSet):
    """
    获取指定日期的文章列表
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = PageNum

    def archiveArticles(self, request, date):
        queryset = Article.objects.filter(create_date__icontains=date).order_by('-create_date')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TagList(ModelViewSet):
    """
    获取文章标签列表
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagArticles(ModelViewSet):
    """
    获取指定标签的文章列表
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = PageNum

    def tagArticles(self, request, tag):
        tags = Tag.objects.filter(id=tag)
        queryset = Article.objects.filter(tags=tags).order_by('-create_date')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TimelineViews(ModelViewSet):
    """
    获取时间轴列表类
    """
    queryset = Article.objects.filter().order_by('-create_date')
    serializer_class = TimeLineSerializer


class ArticleSearch(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = PageNum

    def search(self, request, keyword):
        queryset = Article.objects.filter(body__icontains=keyword).order_by('-create_date')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BlogFeed(Feed):
    # 标题
    title = settings.SITE_DESCRIPTION
    # 描述
    description = '一个用来记录技术的个人博客'
    # 链接
    link = "/"

    def items(self):
        # 返回所有文章
        return Article.objects.all()

    def item_title(self, item):
        # 返回文章标题
        return item.title

    def item_description(self, item):
        # 返回文章内容
        return item.body[:30]

    def item_link(self, item):
        # 返回文章详情页的路由
        return "http://www.hanshouzhi.com/#/detail/" + str(item.id)
