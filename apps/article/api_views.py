import markdown
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.article.article_serializers import ArticleListSerializer, ArticleSerializer, CategorySerializer
from apps.article.models import Article, Category


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
        categories = Article.objects.filter(category__name=name)
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
    获取指定分类的文章列表
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def love(self, request, pk):
        article = Article.objects.filter(id=pk)[0]
        article.loves += 1
        article.save()
        ser = ArticleSerializer(article)
        return Response(ser.data)
