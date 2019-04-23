from django.views.generic.list import ListView

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
