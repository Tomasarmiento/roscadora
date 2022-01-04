from django.urls import path, re_path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('', views.manual, name="manual"),
]