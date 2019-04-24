from django.views.generic.list import ListView

from rentals.models import RentProperty, Availability
from rentals.forms import AvailabilityForm

from ui.views.base_views import PublicReactView, BaseContextMixin


class OldHome(PublicReactView):
    title = 'Home'
    component = 'pages/home.js'
    template = 'ui/home.html'


class Home(BaseContextMixin, ListView):
    title = 'Home'
    template_name = 'ui/home.html'
    model = RentProperty


class Schedule(BaseContextMixin, ListView):
    title = 'Schedule'

    def get_queryset(self):
        return Availability.objects.filter(agent=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AvailabilityForm()
        return context

    def post(self, request, *args, **kwargs):
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)
