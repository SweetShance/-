from django.shortcuts import render, redirect
from django.views import View
from django.contrib import auth
from django.http import JsonResponse
from dataManagement.models import Student
from .models import MyUser


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
        user_username = MyUser.objects.filter(username=username).exists()
        user_email = MyUser.objects.filter(email=email).exists()
        if user_username:
            return JsonResponse({"status": "该用户已被注册"})
        elif user_email:
            return JsonResponse({"status": "该邮箱已被注册"})
        else:
            user = MyUser.objects.create_user(username=username, password=password, email=email)
            user_for_student = Student.objects.filter(sno=user.username)
            if user_for_student:
                user_for_student[0].registerStatus = True
            auth.login(request, user)
            return JsonResponse({"status": "成功"})


# 退出
class Logout(View):
    def get(self, request):
        if request.user:
            auth.logout(request)
        return redirect("MyUser:login")
