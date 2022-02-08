from urllib import request
from django.views.generic.list import ListView
from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from apps.parameters.models import Parameter
from apps.parameters.utils import variables as param_vars




class ParameterListView(ListView):

    model = Parameter
    # paginate_by = 3  # if pagination is desired
    template_name = 'parametrosP1.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("get successful")
        # context['now'] = timezone.now()
        return context


class ParameterView(View):

    def post(request):
        post_req = request.POST
        req_data = {}
        
        for item in post_req.items():   # Item is in (key, value) format
            req_data[item[0]] = item[1]

        print(req_data)
        part_model = req_data['part_model']
        param_vars.SELECTED_MODEL = part_model
        parameters = Parameter.objects.filter(part_model=part_model)
        for param in parameters:
            if req_data.get(param.name, None):
                param.value = req_data[param.name]
                param.save()
                param_vars.PARAMS[param.name] = param.value

        response = HttpResponse()
        response.status_code = 200
        return render(request, 'parameters.html')
    
    def get(request):
        return render(request, 'parameters.html')


def update_parameters(request):
    if request.method == 'POST':
        post_req = request.POST
        req_data = {}
        
        for item in post_req.items():   # Item is in (key, value) format
            req_data[item[0]] = item[1]

        print(req_data)
        part_model = req_data['part_model']
        param_vars.SELECTED_MODEL = part_model
        parameters = Parameter.objects.filter(part_model=part_model)
        for param in parameters:
            if req_data.get(param.name, None):
                param.value = req_data[param.name]
                param.save()
                param_vars.PARAMS[param.name] = param.value

        response = HttpResponse()
        response.status_code = 200
    return render(request, 'parameters.html')


    
