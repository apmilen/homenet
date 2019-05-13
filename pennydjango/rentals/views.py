from django.views.generic import DetailView

from rentals.models import RentProperty
from ui.views.base_views import BaseContextMixin, PublicReactView


class Listings(PublicReactView):
    title = "Listings"
    component = 'pages/listings.js'

    def context(self, request, *args, **kwargs):
        return {'search': request.GET.get('search')}

    def props(self, request, *args, **kwargs):
        query_filter = {'is_listed': True}

        search_param = request.GET.get('search')
        if search_param:
            query_filter.update({'address__icontains': search_param})

        rent_properties = RentProperty.objects.filter(**query_filter)

        return {
            'listings': [rp.__json__() for rp in rent_properties]
        }


class ListingDetail(BaseContextMixin, DetailView):
    model = RentProperty
    template_name = 'rentals/listing_detail.html'
