from urllib import request
from django.views.generic.list import ListView
from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from apps.parameters.models import Parameter
from apps.parameters.utils import variables as param_vars
from apps.parameters.utils import functions as param_func



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

    def post(self, request):
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
        
        param_func.update_homing_params()
        param_func.update_roscado_params()
        
        return render(request, 'parameters.html', self.get_context())
    
    def get(self, request):
        context = self.get_context()
        return render(request, 'parameters.html', context)
    
    def get_context(self):
        params = Parameter.objects.all()
        context = {}
        homming_params = []
        for option in param_vars.PART_MODEL_OPTIONS:
            f_params = params.filter(part_model=option)
            ctx_params = []
            for name in param_vars.PARAM_NAMES:
                print('PARAM NAME:', name)
                param = f_params.get(name=name)
                ctx_params.append({
                    'name': name,
                    'description': param.description,
                    'value': param.value,
                    'unit': param.unit
                })
            option_key = 'model_' + str(option)
            context[option_key] = ctx_params
        
        f_params = params.filter(part_model=0)
        for name in param_vars.HOMING_PARAM_NAMES:
            param = f_params.get(name=name)
            homming_params.append({
                    'name': name,
                    'description': param.description,
                    'value': param.value,
                    'unit': param.unit
                })
        context['model_0'] = homming_params
        return context



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


    
