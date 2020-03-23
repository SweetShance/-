from django.shortcuts import render
from django.views import View
from django.contrib import auth
from django.http import JsonResponse


# Create your views here.
class Login(View):
    def get(self, request):
        return render(request, template_name="MyUser/pages-signin.html", context={})

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
