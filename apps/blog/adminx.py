from extra_apps import xadmin

# Register your models here.
from apps.blog.models import About, Message


class AboutAdmin(object):
    # 这个的作用是给出一个筛选机制，一般按照时间比较好
    date_hierarchy = 'create_date'


class MessageAdmin(object):
    readonly_fields = ['body', 'create_date']


xadmin.site.register(About, AboutAdmin)
xadmin.site.register(Message, MessageAdmin)
