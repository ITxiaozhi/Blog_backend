import markdown
from datetime import datetime

from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from Blog_backend import settings
from apps.blog.blog_serializers import AboutSerializer, MessageSerializer
from apps.blog.models import About, Message


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


class MessageViews(ModelViewSet):
    """
    保存读者留言
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        body = data.get('body', '')
        create_date = data.get('create_date', datetime.now())

        # 发送邮件
        ret = send_mail(subject=settings.EMAIL_SUBJECT, message=body, from_email=settings.EMAIL_FROM,
                  recipient_list=settings.EMAIL_HOST_RECEIVER)
        try:
            # 添加数据库
            message = Message.objects.create(body=body, create_date=create_date)
        except Exception as e:
            print(e)
            return Response(status=500)
        ser = MessageSerializer(message)
        return Response(ser.data, status=201)
