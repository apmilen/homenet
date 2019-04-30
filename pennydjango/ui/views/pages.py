from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin, DeleteView

from penny.models import Availability
from penny.forms import AvailabilityForm

from rentals.models import RentProperty

from ui.views.base_views import PublicReactView, BaseContextMixin


class OldHome(PublicReactView):
    title = 'Home'
    component = 'pages/home.js'
    template = 'ui/home.html'


class Home(BaseContextMixin, ListView):
    title = 'Home'
    template_name = 'ui/home.html'
    model = RentProperty
    search_value = ''

    def get(self, request, *args, **kwargs):
        self.search_value = self.request.GET.get('search')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        value = self.search_value
        self.queryset = super().get_queryset()
        if value:
            self.queryset = self.queryset.filter(address__icontains=value)
        return self.queryset

    def context(self, request, *args, **kwargs):
        return {'search': self.search_value}


class Schedule(BaseContextMixin, FormMixin, ListView):
    title = 'Schedule'
    form_class = AvailabilityForm
    template_name = 'penny/schedule.html'

    def get_queryset(self):
        return Availability.objects.filter(agent=self.request.user)

    def context(self, request, *args, **kwargs):
        return {'form': self.get_form()}

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('home'))

        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('schedule')

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.agent = request.user
            obj.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ScheduleDelete(DeleteView):
    model = Availability

    def get_success_url(self):
        return reverse('schedule')

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        return self.delete(request, *args, **kwargs)
