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
from .adminViews import MeetingManage, ImportStudent, Download_student_xls, AssignTables, MeetingSeting
from .views import MeetingStudent

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('xadmin/meetingSetting/', MeetingSeting.as_view()),
    path('xadmin/meetingManage/', MeetingManage.as_view()),
    path('xadmin/assignTables/', AssignTables.as_view()),
    path('xadmin/importStudent/', ImportStudent.as_view()),
    path('xadmin/downloadStudentXls/', Download_student_xls.as_view()),
    path('meetingStudents/', MeetingStudent.as_view(), name="meetingStudents")

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)