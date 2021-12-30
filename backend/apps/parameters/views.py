from django.views.generic.list import ListView

from apps.parameters.models import Parameter

class ParameterListView(ListView):

    model = Parameter
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        return context