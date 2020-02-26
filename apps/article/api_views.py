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
    ordering_fields = ('update_date',)


# class ArticleViews(ModelViewSet):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer

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
            article = ''
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

    def categoryArticles(self, request, pk):
        categories = Article.objects.filter(category=pk)
        ser = ArticleSerializer(categories, many=True)
        return Response(ser.data)
