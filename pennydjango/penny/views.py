from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, UpdateView

from penny.forms import GeneralSettingsForm
from penny.models import User
from penny.mixins import AdminRequiredMixin
from datatables_listview.core.views import DatatablesListView


class UsersList(AdminRequiredMixin, DatatablesListView, TemplateView):
    model = User
    table_name = 'Users'
    template_name = 'penny/datatables.html'
    fields = ('username', 'first_name', 'last_name', 'email')
    column_names_and_defs = ('Username', 'First Name', 'Last Name', 'Email')
    options_list = [
        {
            'option_label': 'Detail',
            'option_url': 'userprofile',
            'url_params': ['username'],
            'icon': 'user'
        }
    ]


class GeneralSettingsView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = GeneralSettingsForm
    template_name = 'penny/user_settings/_base.html'

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Profile info updated"
        )
        return reverse('penny:user_settings')

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, id=self.request.user.id)


class PasswordSettingsView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'penny/user_settings/_base.html'

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Password updated"
        )
        return reverse('penny:user_password')

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, id=self.request.user.id)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        del kwargs['instance']
        kwargs.update({'user': self.object})
        return kwargs

    def form_valid(self, form):
        updated_user = form.save()
        update_session_auth_hash(self.request, updated_user)
        return HttpResponseRedirect(self.get_success_url())
