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
