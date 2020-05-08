from django.urls import path
from .views import Login, Register, Logout, SendEmail

app_name = "MyUser"
urlpatterns = [
    path("", Login.as_view(), name="login"),
    path("register/", Register.as_view(), name="register"),
    path("logout/", Logout.as_view(), name="logout"),
    path("sendEmail/", SendEmail.as_view(), name="sendEmail"),
]
