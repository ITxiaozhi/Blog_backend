import markdown

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.blog.blog_serializers import AboutSerializer
from apps.blog.models import About


class AboutViews(APIView):
    """
    获取关于自己类
    """

    def get(self, request):
        """
        获取关于自己
        """

        try:
            queryset = About.objects.all()[0]
        except About.DoesNotExist:
            return Response('404')
        # 将body转成Markdown格式
        queryset.body = markdown.markdown(queryset.body,
                                         extensions=[
                                             'markdown.extensions.extra',
                                             'markdown.extensions.codehilite',
                                             'markdown.extensions.toc',
                                         ])
        serializer = AboutSerializer(queryset)

        return Response(serializer.data)

