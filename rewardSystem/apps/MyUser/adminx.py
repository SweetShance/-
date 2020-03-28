import xadmin
from .models import MyUser


class MyUserAdmin(object):
    list_display = ['id', 'username', 'name', 'phone', 'email', 'identity']
    # 过滤器
    list_filter = ["username", 'identity']

    # 查询
    search_fields = ["name", "username"]
    # fieldsets = [
    #     # 对成员变量进行分类
    #     ('基本信息', {'fields': ["username", "name", "phone", "email", "date_join", "last_login",]}),
    #     # ('名字', {'fields': ['成员变量']})
    # ]
    fields = ["username", "name", "phone", "email", "date_joined", "last_login", "groups", "user_permissions", "identity", "is_active", "is_superuser", "is_staff"]
    # fieldsets = [
    #     ('基本信息', {
    #        "fields": ("username", "name", "phone", "email", "date_join", "last_login",)
    #     }),
    #     ('用户权限', {
    #         "fields": ("groups", "user_permissions", "is_active", "is_superuser", "is_staff")
    #     })
    # ]

    # 每页显示行数
    list_per_page = 30
    model_icon = 'fa fa-user'


xadmin.site.unregister(MyUser)
xadmin.site.register(MyUser, MyUserAdmin)
