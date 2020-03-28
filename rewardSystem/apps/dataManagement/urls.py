from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import Index, MyInfo, SetPassword, RequestLog, RequestLogShow, ApplicationFormUpload,\
    DeleteAll, DeleteOne


app_name = "dataManagement"
urlpatterns = [
    path("index/", login_required(Index.as_view()), name="index"),
    path("myinfo/", login_required(MyInfo.as_view()), name="myinfo"),
    path("setPassword/", login_required(SetPassword.as_view()), name="setPassword"),
    path("requestLog/", login_required(RequestLog.as_view()), name="requestLog"),
    path("requestLogShow/", login_required(RequestLogShow.as_view()), name="requestLogShow"),
    path("applicationFormUpload/", login_required(ApplicationFormUpload.as_view()), name="applicationFormUpload"),
    path("deleteOne/", login_required(DeleteOne.as_view()), name="deleteOne"),
    path("dedleteAll/", login_required(DeleteAll.as_view()), name="deleteAll")
]