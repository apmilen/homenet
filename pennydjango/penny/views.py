from django.views.generic import TemplateView

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
