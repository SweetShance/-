from django.urls import path
from .views import Login

app_name = "MyUser"
urlpatterns = [
    path("login/", Login.as_view(), name="login")
]