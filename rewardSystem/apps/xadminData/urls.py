from django.urls import path
from xadminData.views import MeetingDeleteStudent, MeetingAddStudentList, MeetingAddStudent, MeetingImportAddStudent,\
    MeetingImportDeleteStudent, MeetingImportChangeStudent, MeetingImportChangeStudentSave

app_name = "xadminData"
urlpatterns = [
    path("meetingDeleteStudent/", MeetingDeleteStudent.as_view(), name="meetingDeleteStudent"),
    # 添加学生的学生列表, 用来做局部刷新
    path("meetingAddStudentList/", MeetingAddStudentList.as_view(), name="meetingAddStudentList"),
    # 添加学生
    path("meetingAddStudent/", MeetingAddStudent.as_view(), name="meetingAddStudent"),
    # 添加不符合资格学生
    path("meetingimportAddStudent/", MeetingImportAddStudent.as_view(), name="meetingimportAddStudent"),
    path("meetingImportDeleteStudent/", MeetingImportDeleteStudent.as_view(), name="meetingImportDeleteStudent"),
    path("meetingImportChangeStudent/", MeetingImportChangeStudent.as_view(), name="meetingImportChangeStudent"),
    path("meetingImportChangeSave/", MeetingImportChangeStudentSave.as_view(), name="meetingImportChangeSave")


]