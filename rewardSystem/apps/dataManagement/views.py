from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class Index(View):
    def get(self, request):
        print(request.user, "hello")
        return render(request, template_name="dataManagement/index.html", context={})