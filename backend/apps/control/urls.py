from django.urls import path, re_path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('manual/motor/', views.manual_lineal, name='manual-motor'),
    path('manual/neummatica/', views.manual_pneumatic, name='manual-pneumatic'),
    path('manual/stop-axis/', views.stop_axis, name='stop-axis')
]