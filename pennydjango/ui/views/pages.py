from django.conf import settings
from django.views.generic.list import ListView

from ui.views.base_views import PublicReactView, BaseContextMixin

from listings.models import Listing
from listings.constants import PETS_ALLOWED, AMENITIES, LISTING_TYPES

from penny.constants import NEIGHBORHOODS


class Home(PublicReactView):
    title = "Home"
    component = 'pages/home.js'

    def props(self, request, *args, **kwargs):
        constants = {
            'pets_allowed': dict(PETS_ALLOWED),
            'amenities': {
                amenity_tuple[0]: amenity_tuple[1]
                for _, group in dict(AMENITIES).items()
                for amenity_tuple in group
            },
            'neighborhoods': dict(NEIGHBORHOODS),
            'listing_types': dict(LISTING_TYPES),
        }
        return {
            'map_key': settings.MAPBOX_API_KEY,
            'constants': constants,
            'endpoint': '/listings/public/',
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
