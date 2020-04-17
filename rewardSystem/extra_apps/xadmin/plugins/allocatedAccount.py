import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView
from django.template import loader
from xadmin.plugins.utils import get_context_dict


# 分配账户
class ListAllocatedAccountPlugin(BaseAdminPlugin):
    allocated_account = False

    # 入口函数, 通过此属性来指定此字段是否加载此字段
    def init_request(self, *args, **kwargs):
        return bool(self.allocated_account)

    # 如果加载, 则执行此函数添加一个导入字段
    def block_top_toolbar(self, context, nodes):
        context = get_context_dict(context or {})
        nodes.append(
            loader.render_to_string('xadmin/allocated/model_list.top_toolbar.allocated_account.html', context=context))


xadmin.site.register_plugin(ListAllocatedAccountPlugin, ListAdminView)

# # excel 导入
# class ListAllocatedAccountPlugin(BaseAdminPlugin):
#     # 设置功能开关
#     allocated_account = False
#
#     # 入口函数, 通过此属性来指定此字段是否加载此字段
#     def init_request(self, *args, **kwargs):
#         return bool(self.allocated_account)
#
#     # 如果加载, 则执行此函数添加一个 导入 字段
#     def block_top_toolbar(self, context, nodes):
#         nodes.append(
#             loader.render_to_string("xadmin/allocated/model_list.top_toolbar.allocated_account.html", context=context))
#
#
# xadmin.site.register_plugin(ListAllocatedAccountPlugin, ListAdminView)