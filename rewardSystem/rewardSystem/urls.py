"""rewardSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static   # 新加入
from django.conf import settings             # 新加入
import xadmin
from .adminViews import MeetingManage, ImportStudent, Download_student_xls, AssignTables, MeetingSetting, AllotJury, JuryList, ImportStudentGrade,\
        StatisticsQuestion, StatisticsResult
from .views import MeetingStudent

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('xadmin/meetingSetting/', MeetingSetting.as_view()),
    path('xadmin/meetingManage/', MeetingManage.as_view()),
    path('xadmin/assignTables/', AssignTables.as_view()),
    # 导入学生成绩
    path('xadmin/importStudent/', ImportStudent.as_view()),
    path('xadmin/importStudentGrade/', ImportStudentGrade.as_view(), name="importStudentGrade"),
    path('xadmin/downloadStudentXls/', Download_student_xls.as_view()),
    path('meetingStudents/', MeetingStudent.as_view(), name="meetingStudents"),
    path('xadminData/', include("xadminData.urls")),
    # 评委列表
    path('xadmin/juryList/', JuryList.as_view(), name="juryList"),
    # 分配评委
    path("xadmin/allotJury/", AllotJury.as_view(), name="allotJury"),
    # 会议统计 问题
    path("xadmin/statisticsQuestion/", StatisticsQuestion.as_view(), name="statisticsQuestion"),
    # 会议统计 结果
    path("xadmin/statisticsResult/", StatisticsResult.as_view(), name="statisticsResult"),
    # 登录注册以及用户信息
    path("user/", include("MyUser.urls")),
    path("dataManagement/", include("dataManagement.urls")),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)