import xadmin
from .models import MyUser


class MyUserAdmin(object):
    list_display = ['id', 'username', 'name', 'phone', 'email', 'identity']
    # 过滤器
    list_filter = ["username", 'identity']

    # 查询
    search_fields = ["name", "username"]

    # 每页显示行数
    list_per_page = 30
    model_icon = 'fa fa-user'


xadmin.site.unregister(MyUser)
xadmin.site.register(MyUser, MyUserAdmin)
