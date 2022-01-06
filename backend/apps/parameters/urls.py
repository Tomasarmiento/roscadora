from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.ParameterListView.as_view(), name="parameters-list"),
<<<<<<< HEAD
    path('update/<int:part_model>', views.update, name="parameter-update")
=======
    path('update', views.update_parameters, name="parameters-update")
>>>>>>> parameters
]