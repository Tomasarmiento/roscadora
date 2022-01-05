from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.shortcuts import redirect, reverse

from apps.service.api.variables import COMMANDS
from apps.parameters.utils.variables import PART_MODEL_OPTIONS

# Create your views here.
def index(request):
    return render(request, "index.html")
  
def home(request):
    return render(request, "home.html")

def referenciar(request):
    return render(request, "referenciar.html")

def automatico(request):
    return render(request, "automatico.html")

def neumaticaManual(request):
    return render(request, "neumaticaManual.html")

def motoresManual(request):
    return render(request, "motoresManual.html", context=COMMANDS)

def sensores(request):
    return render(request, "sensores.html")

def monitorEstados(request):
    return render(request, "monitorEstados.html")

def semiAutomatico(request):
    return render(request, "semiautomatico.html")

def parametrosPagina1(request):
    d = {}
    for i in range(len(PART_MODEL_OPTIONS)):
        d[i+1] = PART_MODEL_OPTIONS[0]
    return render(request, "parametrosP1.html", d)

def parametrosPagina2(request):
    return render(request, "parametrosP2.html")