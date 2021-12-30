from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.ParameterListView.as_view(), name="parameters-list")
]