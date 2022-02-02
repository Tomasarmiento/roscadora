from django.urls import path, re_path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('manual/motor/', views.manual_lineal, name='manual-motor'),
    path('manual/motor/enable/', views.enable_axis, name='enable-axis'),
    path('manual/motor/sync/', views.sync_axis, name='sync-axys'),
    path('manual/neummatica/', views.manual_pneumatic, name='manual-pneumatic'),
    path('semiautomatico/', views.semiauto, name='semiauto'),
    path('manual/stop-axis/', views.stop_axis, name='stop-axis'),
    path('stop-all/', views.stop_all, name='stop-all'),
    path('auto/', views.StartRoutine.as_view(), name='auto')
]