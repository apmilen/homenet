from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

from penny.models import User
from penny.forms import CustomUserCreationForm

from ui.views.base_views import BaseContextMixin


class Signup(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())


class UserProfile(BaseContextMixin, DetailView):
    model = User
    custom_stylesheet = 'user.css'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def context(self, request, *args, **kwargs):
        is_me = self.object == request.user
        return {'is_me': is_me}
