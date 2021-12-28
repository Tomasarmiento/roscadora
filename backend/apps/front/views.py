from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.shortcuts import redirect, reverse

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
    return render(request, "motoresManual.html")

def sensores(request):
    return render(request, "sensores.html")

def monitorEstados(request):
    return render(request, "monitorEstados.html")

def semiAutomatico(request):
    return render(request, "semiautomatico.html")

def parametrosPagina1(request):
    return render(request, "parametrosP1.html")

def parametrosPagina2(request):
    return render(request, "parametrosP2.html")