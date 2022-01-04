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

    # Create your views here.
def update_parameters(request):
    if request.method == 'POST': print('hola')
    response = HttpResponse()
    response.status_code = 200
    print(request.body)
    
    param = Parameter.objects.filter(part_model=1)(name='paso_de_rosca')
   # param.value = (request.POST['paso_de_rosca'])
    param.save()
    
    return render(request, "parametrosP1.html")






    