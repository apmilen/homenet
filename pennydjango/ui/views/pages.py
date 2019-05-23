from django.views.generic.list import ListView

from ui.views.base_views import PublicReactView, BaseContextMixin

from listings.models import Listing
from listings.constants import APPROVED


class Home(PublicReactView):
    title = "Listings"
    component = 'pages/listings.js'

    def props(self, request, *args, **kwargs):
        query_filter = {'status': APPROVED}
        listings = Listing.objects.filter(**query_filter)

        return {
            'listings': [listing.__json__() for listing in listings]
        }


class OldHome(BaseContextMixin, ListView):
    title = 'Home'
    template_name = 'ui/home.html'
    model = Listing
    search_value = ''

    def get(self, request, *args, **kwargs):
        self.search_value = self.request.GET.get('search')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        value = self.search_value
        self.queryset = super().get_queryset()
        self.queryset = self.queryset.select_related('detail', 'photos')
        if value:
            self.queryset = self.queryset.filter(address__icontains=value)
        return self.queryset

    def context(self, request, *args, **kwargs):
        return {'search': self.search_value}
