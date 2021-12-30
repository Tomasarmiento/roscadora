from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('referenciar/', views.referenciar, name="referenciar"),
    path('automatico/', views.automatico, name="automatico"),
    path('neumaticaManual/', views.neumaticaManual, name="neumaticaManual"),
    path('motoresManual/', views.motoresManual, name="motoresManual"),
    path('sensores/', views.sensores, name="sensores"),
    path('monitorEstados/', views.monitorEstados, name="monitorEstados"),
    path('semiAutomatico/', views.semiAutomatico, name="semiAutomatico"),
    path('parametrosPagina1/', views.parametrosPagina1, name="parametrosPagina1"),
    path('parametrosPagina2/', views.parametrosPagina2, name="parametrosPagina2"),
]