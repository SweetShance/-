from django.shortcuts import render, redirect
from django.views import View
from django.contrib import auth
from django.http import JsonResponse
import random, datetime
from dataManagement.models import Student
from .models import MyUser, UserCode
from .task import send_register_active_email


# Create your views here.
class Login(View):
    def get(self, request):
        return render(request, template_name="MyUser/login.html", context={})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({"status": "用户名密码错误"})
        else:
            if user.is_active:
                auth.login(request, user)
            return JsonResponse({"status": "成功"})


# 注册
class Register(View):
    def get(self, request):

        return render(request, template_name="MyUser/register.html", context={})

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        code = request.POST.get("code")
        user_username = MyUser.objects.filter(username=username).exists()
        user_email = MyUser.objects.filter(email=email).exists()
        userCode = UserCode.objects.filter(username=username, code=code).order_by("-date")
        if user_username:
            return JsonResponse({"status": "该用户已被注册"})
        elif user_email:
            return JsonResponse({"status": "该邮箱已被注册"})
        elif not userCode:
            return JsonResponse({"status": "验证码错误"})
        else:
            timing = (datetime.datetime.now() - userCode[0].date).total_seconds() / 60
            if timing > 5:
                return JsonResponse({"status": "验证码失效"})
            else:
                user = MyUser.objects.create_user(username=username, password=password, email=email)
                user_for_student = Student.objects.filter(sno=user.username)
                if user_for_student:
                    user_for_student[0].registerStatus = True
                    user.name = user_for_student[0].sname
                    user.save()
                auth.login(request, user)
                return JsonResponse({"status": "成功"})


# 退出
class Logout(View):
    def get(self, request):
        if request.user:
            auth.logout(request)
        return redirect("MyUser:login")


# 发送邮箱
class SendEmail(View):
    def post(self, request):
        email = request.POST.get("email")
        username = request.POST.get("username")
        user_username = MyUser.objects.filter(username=username).exists()
        user_email = MyUser.objects.filter(email=email).exists()
        if user_username:
            return JsonResponse({"status": "该用户已被注册"})
        elif user_email:
            return JsonResponse({"status": "该邮箱已被注册"})
        else:
            # 生成验证码
            ret = ""
            for i in range(5):
                num = random.randint(0, 9)
                alf = chr(random.randint(97, 122))
                s = str(random.choice([num, alf]))
                ret += s
            # 把数据存到数据库
            if email and username:
                send_register_active_email(email, ret.strip())
                UserCode.objects.create(username=username, code=ret.strip(), email=email)
                return JsonResponse({"status": "发送成功"})
            else:
                return JsonResponse({"status": "邮箱存在问题"})