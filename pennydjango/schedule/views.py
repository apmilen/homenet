from django.urls import reverse
from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from schedule.models import Availability
from schedule.forms import AvailabilityForm
from ui.views.base_views import BaseContextMixin


class Schedule(LoginRequiredMixin, BaseContextMixin, FormMixin, ListView):
    title = 'Schedule'
    form_class = AvailabilityForm
    template_name = 'penny/schedule.html'

    def get_queryset(self):
        # return Availability.objects.filter(agent=self.request.user)
        return Availability.objects.all()

    def context(self, request, *args, **kwargs):
        return {'form': self.get_form()}

    def get_success_url(self):
        return reverse('schedule')

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.agent = request.user
            obj.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ScheduleDelete(LoginRequiredMixin, DeleteView):
    model = Availability

    def get_success_url(self):
        return reverse('schedule')

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not obj.agent == self.request.user:
            raise Http404
        return obj
