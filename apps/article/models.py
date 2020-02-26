import markdown
from django.db import models
from mdeditor.fields import MDTextField

# Create your models here.
# 文章关键词，用来作为 SEO 中 keywords
from django.urls import reverse

from myblog import settings

# 文章标签
class Tag(models.Model):
    name = models.CharField('文章标签', max_length=20)
    description = models.TextField('描述', max_length=240, default=settings.SITE_DESCRIPTION,
                                 help_text='用来作为SEO中description,长度参考SEO标准')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name


# 网站导航菜单栏分类表
class BigCategory(models.Model):
    name = models.CharField('文章大分类', max_length=20)

    description = models.TextField('描述', max_length=240, default=settings.SITE_DESCRIPTION,
                                 help_text='用来作为SEO中description,长度参考SEO标准')

    class Meta:
        verbose_name = '大分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 导航栏，分类下的下拉擦菜单分类
class Category(models.Model):
    name = models.CharField('文章分类', max_length=20)
    description = models.TextField('描述', max_length=240, default=settings.SITE_DESCRIPTION,
                                 help_text='用来作为SEO中description,长度参考SEO标准')
    bigcategory = models.ForeignKey(BigCategory, verbose_name='大分类')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


# 文章
class Article(models.Model):
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者')
    title = models.CharField(max_length=150, verbose_name='文章标题')
    summary = models.TextField('文章摘要', max_length=230, default='文章摘要等同于网页description内容，请务必填写...')
    # body = models.TextField(verbose_name='文章内容')
    body = MDTextField(verbose_name='文章内容')
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    views = models.IntegerField('阅览量', default=0)
    loves = models.IntegerField('喜爱量', default=0)
    category = models.ForeignKey(Category, verbose_name='文章分类')
    tags = models.ManyToManyField(Tag, verbose_name='标签')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']

    def __str__(self):
        return self.title[:20]

# 幻灯片
class Carousel(models.Model):
    number = models.IntegerField('编号', help_text='编号决定图片播放的顺序，图片不要多于5张')
    title = models.CharField('标题', max_length=20, blank=True, null=True, help_text='标题可以为空')
    content = models.CharField('描述', max_length=80)
    img_url = models.CharField('图片地址', max_length=200)
    url = models.CharField('跳转链接', max_length=200, default='#', help_text='图片跳转的超链接，默认#表示不跳转')

    class Meta:
        verbose_name = '图片轮播'
        verbose_name_plural = verbose_name
        # 编号越小越靠前，添加的时间约晚约靠前
        ordering = ['number', '-id']

    def __str__(self):
        return self.content[:25]
