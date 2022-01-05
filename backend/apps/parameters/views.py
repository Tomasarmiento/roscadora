from asyncio.windows_events import NULL
from django.db.models.expressions import Value
from django.views.generic.list import ListView
from django.shortcuts import render
from apps.parameters.models import Parameter
from django.http import HttpResponse




class ParameterListView(ListView):

    model = Parameter
    # paginate_by = 3  # if pagination is desired
    template_name = 'parametrosP1.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("get successful")
        # context['now'] = timezone.now()
        return context


def update_parameters(request):
    if request.method == 'POST': 
        response = HttpResponse()
        response.status_code = 200
        print(request.body)
        
    return render(request, 'parametrosP1.html')

    
# def save_params(name, part_model, value):
#     param = Parameter.objects.filter(part_model=part_model).get(name=name)
#     param.value = value
#     if value != 0:
#         param.save()
#    ##########################################  MODELO 1 ###################################################
#     save_params(part_model=1, name='torque_tolerado', value=request.POST['torque_tolerado']or NULL)
#     save_params(part_model=1, name='paso_de_rosca', value=request.POST['paso_de_rosca']or NULL)
#     save_params(part_model=1, name='posicion_de_aprox', value=request.POST['posicion_de_aprox']or NULL)
#     save_params(part_model=1, name='velocidad_de_aprox', value=request.POST['velocidad_de_aprox']or NULL)
#     save_params(part_model=1, name='distancia_de_roscado', value=request.POST['distancia_de_roscado']or NULL)
#     save_params(part_model=1, name='velocidad_de_roscado', value=request.POST['velocidad_de_roscado']or NULL)
#     save_params(part_model=1, name='velocidad_de_retraccion', value=request.POST['velocidad_de_retraccion']or NULL)
#     save_params(part_model=1, name='tiempo_de_ciclo', value=request.POST['tiempo_de_ciclo']or NULL)
#     save_params(part_model=1, name='t_inicio_soluble', value=request.POST['t_inicio_soluble']or NULL)
#    ##########################################  MODELO 2 ###################################################
#     save_params(part_model=2, name='torque_tolerado', value=request.POST['torque_tolerado'] or NULL)
#     save_params(part_model=2, name='paso_de_rosca', value=request.POST['paso_de_rosca'] or NULL)
#     save_params(part_model=2, name='posicion_de_aprox', value=request.POST['posicion_de_aprox'] or NULL)
#     save_params(part_model=2, name='velocidad_de_aprox', value=request.POST['velocidad_de_aprox'] or NULL)
#     save_params(part_model=2, name='distancia_de_roscado', value=request.POST['distancia_de_roscado'] or NULL)
#     save_params(part_model=2, name='velocidad_de_roscado', value=request.POST['velocidad_de_roscado'] or NULL)
#     save_params(part_model=2, name='velocidad_de_retraccion', value=request.POST['velocidad_de_retraccion'] or NULL)
#     save_params(part_model=2, name='tiempo_de_ciclo', value=request.POST['tiempo_de_ciclo'] or NULL)
#     save_params(part_model=2, name='t_inicio_soluble', value=request.POST['t_inicio_soluble'] or NULL)



    