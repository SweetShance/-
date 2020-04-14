from __future__ import absolute_import
import xadmin
from .models import UserSettings, Log
from xadmin import views

from xadmin.layout import *

from django.utils.translation import ugettext_lazy as _, ugettext


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSetting)  # 注册到xadmin中


class GlobalSetting(object):
    # 设置base_site.html的Title
    site_title = '后台管理'
    # 设置base_site.html的Footer
    site_footer = '我的脚丫'
    menu_style = 'accordion'

    def get_site_menu(self):
        return [
            {
                'title': '赋分表',
                'menus': (
                    {
                        'title': '分配赋分表',
                        'url': '/xadmin/assignTables'
                    },
                )
            },
            {
                'title': "会议管理",
                # # 'icon': 'fa fa-bar-chart-o',
                'menus': (
                    {
                        'title': '会议设置',
                        'url': '/xadmin/meetingManage'
                    },
                )
            },
        ]


from rewardSystem.adminViews import MeetingManage, ImportStudent, Download_student_xls, AssignTables, \
    MeetingSetting, AllotJury, JuryList
# 注册自定义分配赋分表页面
xadmin.site.register_view('meetingManage', MeetingManage, name='meetingManage')
# 分配赋分表
xadmin.site.register_view("assignTables", AssignTables, name='assignTables')
# 会议设置页面
xadmin.site.register_view('meetingSetting', MeetingSetting, name="meetingSetting")
# 评委列表
xadmin.site.register_view('juryList', JuryList, name="juryList")
# 分配评委
xadmin.site.register_view('allotJury', AllotJury, name="allotJury")
xadmin.site.register_view('importStudent', ImportStudent, name="importStudent")
xadmin.site.register_view('downloadStudent', Download_student_xls, name="downloadStudent")

# 注册F
xadmin.site.register(xadmin.views.CommAdminView, GlobalSetting)


class UserSettingsAdmin(object):
    model_icon = 'fa fa-cog'
    hidden_menu = True


xadmin.site.register(UserSettings, UserSettingsAdmin)


class LogAdmin(object):

    def link(self, instance):
        if instance.content_type and instance.object_id and instance.action_flag != 'delete':
            admin_url = self.get_admin_url(
                '%s_%s_change' % (instance.content_type.app_label, instance.content_type.model),
                instance.object_id)
            return "<a href='%s'>%s</a>" % (admin_url, _('Admin Object'))
        else:
            return ''

    link.short_description = ""
    link.allow_tags = True
    link.is_column = False

    list_display = ('action_time', 'user', 'ip_addr', '__str__', 'link')
    list_filter = ['user', 'action_time']
    search_fields = ['ip_addr', 'message']
    model_icon = 'fa fa-cog'


xadmin.site.register(Log, LogAdmin)
