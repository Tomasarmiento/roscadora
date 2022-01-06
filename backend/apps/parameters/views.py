from asyncio.windows_events import NULL
from django.db.models.expressions import Value
from django.views.generic.list import ListView
from django.shortcuts import render
from apps.parameters.models import Parameter
from django.http import HttpResponse, HttpResponseRedirect




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
        post_req = request.POST
        part_model = post_req['part_model']
        parameters = Parameter.objects.filter(part_model=part_model)
        for param in parameters:
            if post_req[param.name]:
                param.value = post_req[param.name]
                param.save()
        response = HttpResponse()
        response.status_code = 200
        
    return render(request, 'parametrosP1.html')


    