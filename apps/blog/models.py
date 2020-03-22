from django.db import models

# Create your models here.
from mdeditor.fields import MDTextField


class About(models.Model):
    body = MDTextField(verbose_name='关于自己内容')
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        verbose_name = '关于自己'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.body[:20]


class Message(models.Model):
    body = models.CharField(max_length=150, verbose_name='读者留言')
    create_date = models.DateTimeField(verbose_name='创建时间')

    class Meta:
        verbose_name = '给我留言'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.body[:20]
