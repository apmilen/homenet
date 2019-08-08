from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, UpdateView

from penny.forms import GeneralSettingsForm
from penny.models import User
from penny.mixins import AdminRequiredMixin
from penny.constants import USER_TYPE

from ui.views.base_views import PublicReactView

from datatables_listview.core.views import DatatablesListView


class UsersList(AdminRequiredMixin, DatatablesListView, TemplateView):
    model = User
    table_name = 'Users'
    template_name = 'penny/datatables.html'
    fields = ('first_name', 'last_name', 'email')
    column_names_and_defs = ('First Name', 'Last Name', 'Email')
    options_list = [
        {
            'option_label': 'Detail',
            'option_url': 'userprofile',
            'url_params': ['id'],
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


class Users(AdminRequiredMixin, PublicReactView):
    title = "Users"
    component = 'pages/users.js'

    def props(self, request, *args, **kwargs):
        return {
            'constants': {
                'user_type': dict(USER_TYPE),
            }
        }

    def post(self, request, *args, **kwargs):
        request_type = request.POST.get('type')
        response = {'success': False, 'details': "My job is done"}

        if request_type == 'NEW_USER':
            name = request.POST.get('name')
            email = request.POST.get('email')
            user_type = request.POST.get('user_type')
            response = invite_new_user(name, email, user_type)

        if request_type == 'FILTER_USER':
            users = qs_from_filters(
                User.objects.all(),
                request.POST
            ).order_by('-modified')
            response = {
                'users': [user.__json__() for user in users]
            }

        if request_type == 'UPDATE_USER':
            fields = request.POST.dict().copy()
            fields['is_active'] = (
                True if fields['is_active'] == 'true' else False)
            fields.pop('type', None)
            user_id = fields.pop('id', None)
            print(fields, flush=True)
            response = update_user(user_id, fields)

        return JsonResponse(response)


def update_user(user_id, fields):
    users = User.objects.filter(id=user_id)
    if not users or users.count() > 1:
        return {
            'success': False,
            'details': "User not found",
        }

    users.update(**fields)
    return {
        'success': True,
        'user': users[0].__json__(),
    }


def qs_from_filters(queryset, params):

    searching_text = params.get('searching_text')
    only_active = params.get('only_active')
    user_type = params.get('user_type')

    if searching_text:
        queryset = queryset.filter(
            Q(first_name__icontains=searching_text) |
            Q(last_name__icontains=searching_text) |
            Q(email__icontains=searching_text)
        )

    if only_active == 'true':
        queryset = queryset.filter(is_active=True)

    if user_type and user_type != 'any':
        queryset = queryset.filter(user_type=user_type)

    return queryset


def invite_new_user(name, email, user_type):
    if not (email and user_type):
        return {
            'success': False,
            'details': "Missing required data"
        }

    qs = User.objects.filter(email__iexact=email)
    if qs.exists():
        return {
            'success': False,
            'details': 'Email belongs to registered user. Try another one.'
        }

    new_user = User.objects.create_user(
        email=email,
        password='',
        user_type=user_type,
        first_name=name,
    )

    return {
        'success': True,
        'new_user': new_user.__json__(),
    }
