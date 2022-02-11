from django.shortcuts import render

from apps.service.api.variables import COMMANDS
from apps.parameters.utils.variables import PART_MODEL_OPTIONS
from apps.parameters.models import Parameter
from apps.control.utils.variables import AXIS_IDS, ROUTINE_IDS, ROSCADO_CONSTANTES

# Create your views here.
def index(request):
    return render(request, "index.html")
  
def home(request):
    part_model = Parameter.objects.get(name='part_model')
    return render(request, "home.html", {'part_model': int(part_model.value)})

def referenciar(request):
    context = {'routine': ROUTINE_IDS['cerado']}
    return render(request, "referenciar.html", context)

def automatico(request):
    context = COMMANDS
    context.update(ROSCADO_CONSTANTES)
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
    context.update(ROSCADO_CONSTANTES)
    return render(request, "semiautomatico.html", context)

def parametrosPagina1(request):
    return render(request, "parametrosP1.html")

def logAlarma(request):
    return render(request, "logAlarma.html")
