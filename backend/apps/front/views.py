from django.shortcuts import render

from apps.service.api.variables import COMMANDS
from apps.parameters.utils.variables import PART_MODEL_OPTIONS
from apps.control.utils.variables import AXIS_IDS, ROUTINE_IDS

# Create your views here.
def index(request):
    return render(request, "index.html")
  
def home(request):
    return render(request, "home.html")

def referenciar(request):
    return render(request, "referenciar.html")

def automatico(request):
    context = COMMANDS
    return render(request, "automatico.html", context)

def neumaticaManual(request):
    context = COMMANDS
    return render(request, "neumaticaManual.html", context)

def motoresManual(request):
    context = COMMANDS
    context['id_eje_avance'] = AXIS_IDS['avance']
    context['id_eje_carga'] = AXIS_IDS['carga']
    context['id_eje_giro'] = AXIS_IDS['giro']
    return render(request, "motoresManual.html", context=context)

def sensoresPagina2(request):
    return render(request, "sensoresP2.html")

def sensores(request):
    return render(request, "sensores.html")

def monitorEstados(request):
    return render(request, "monitorEstados.html")

def semiAutomatico(request):
    context = ROUTINE_IDS
    return render(request, "semiautomatico.html", context)

def parametrosPagina1(request):
    return render(request, "parametrosP1.html")
