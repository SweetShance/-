from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import Index


app_name = "dataManagement"
urlpatterns = [
    path("index/", login_required(Index.as_view()), name="index"),
]