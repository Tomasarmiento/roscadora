from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def manual(request):
    print('MANUAL')
    response = HttpResponse()
    response.status_code = 200
    return response