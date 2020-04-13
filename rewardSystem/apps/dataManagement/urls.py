from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import Index, MyInfo, SetPassword, RequestLog, RequestLogShow, ApplicationFormUpload,\
        DeleteOne, PeerAssessment, MeetingList, MeetingForMyStudent, MeetingForMyStudentCheck, JuryGradeMeetingList, \
        JuryGradeMeetingStudentList, JuryStudentApplicationFormShow, NoticListShow, NoticeShow, Download, MessageIndex,\
        MessageShow, EditMessage, EditSearchUser

app_name = "dataManagement"
urlpatterns = [
    path("index/", login_required(Index.as_view()), name="index"),
    path("noticListShow/", login_required(NoticListShow.as_view()), name="noticListShow"),
    path("noticShow/<int:pk>", login_required(NoticeShow.as_view()), name="noticShow"),
    path("downloadNoticeFile/<int:pk>", login_required(Download.as_view()), name="downloadNoticeFile"),
    path("myinfo/", login_required(MyInfo.as_view()), name="myinfo"),
    path("setPassword/", login_required(SetPassword.as_view()), name="setPassword"),
    path("requestLog/", login_required(RequestLog.as_view()), name="requestLog"),
    path("requestLogShow/", login_required(RequestLogShow.as_view()), name="requestLogShow"),
    path("applicationFormUpload/", login_required(ApplicationFormUpload.as_view()), name="applicationFormUpload"),
    path("deleteOne/", login_required(DeleteOne.as_view()), name="deleteOne"),
    path("peerAssessment/", login_required(PeerAssessment.as_view()), name="peerAssessment"),
    # 老师
    # 我的学生
    path("meetingList/", login_required(MeetingList.as_view()), name="meetingList"),
    path("meetingForMyStudent/", login_required(MeetingForMyStudent.as_view()), name="meetingForMyStudent"),
    # 对自己学生审核评分
    path("meetingForMyStudentCheck/", login_required(MeetingForMyStudentCheck.as_view()), name="meetingForMyStudentCheck"),
    path("juryGradeMeetingList/", login_required(JuryGradeMeetingList.as_view()), name="juryGradeMeetingList"),
    # 评委会议学生列表
    path("juryMeetingStudentList/", login_required(JuryGradeMeetingStudentList.as_view()), name="juryMeetingStudentList"),
    # 展示学生申请表和保存赋分
    path("juryStudentApplicationFormShow/", login_required(JuryStudentApplicationFormShow.as_view()), name="juryStudentApplicationFormShow"),
    # 消息
    path("messageIndex/", login_required(MessageIndex.as_view()), name="messageIndex"),
    path("messageShow/<int:pk>", login_required(MessageShow.as_view()), name="messageShow"),
    path("editMessage/", login_required(EditMessage.as_view()), name="editMessage"),
    path("editSearchUser/", login_required(EditSearchUser.as_view()), name="editSearchUser"),

]