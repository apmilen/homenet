from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView

from job_applications.models import JobApplication
from job_applications.forms import JobApplicationForm

class JobApplication(CreateView):
    model = JobApplication
    form_class = JobApplicationForm
    template_name = 'job_applications/job_apply.html'
    success_url = reverse_lazy('home') 

    def form_valid(self, form):
        messages.success(self.request, 'Your job application was submmited')
        return super().form_valid(form)
        