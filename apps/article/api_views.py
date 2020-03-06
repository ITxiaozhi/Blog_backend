import markdown
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.article.article_serializers import ArticleListSerializer, ArticleSerializer, CategorySerializer, \
    ArchiveSerializer, TagSerializer
from apps.article.models import Article, Category, Tag


class ArticleListViews(ModelViewSet):
    """
    获取文章列表类
    """
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ('create_date',)


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

    def categoryArticles(self, request, name):
        categories = Article.objects.filter(category__name=name).order_by('-create_date')
        ser = ArticleSerializer(categories, many=True)
        return Response(ser.data)


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
    queryset = Article.objects.distinct_date()
    serializer_class = ArchiveSerializer


class ArchiveArticles(ModelViewSet):
    """
    获取指定日期的文章列表
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def archiveArticles(self, request, date):
        archives = Article.objects.filter(create_date__icontains=date).order_by('-create_date')
        ser = ArticleSerializer(archives, many=True)
        return Response(ser.data)


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

    def tagArticles(self, request, tag):
        tags = Tag.objects.filter(id=tag)
        article = Article.objects.filter(tags=tags).order_by('-create_date')
        ser = ArticleSerializer(article, many=True)
        return Response(ser.data)
