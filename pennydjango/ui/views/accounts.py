from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView

from penny.models import User
from penny.forms import CustomUserCreationForm


class Signup(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())
