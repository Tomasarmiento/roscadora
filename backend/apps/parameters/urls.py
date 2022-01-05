from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.ParameterListView.as_view(), name="parameters-list"),
    path('update/<int:part_model>', views.update, name="parameter-update")
]