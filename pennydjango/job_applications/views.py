from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import CreateView

from job_applications.models import JobApplication
from job_applications.forms import JobApplicationForm

class JobApplication(CreateView):
    model = JobApplication
    form_class = JobApplicationForm
    template_name = 'job_applications/job_apply.html'

    def post(self, request):
        form = JobApplicationForm(request.POST, request.FILES)
        if request.POST:
            if form.is_valid():
                form.save()
                messages.success(request, 'Your job application was submmited')
                return HttpResponseRedirect('/')
        
        return render(request, 'job_applications/job_apply.html', {'form': form})