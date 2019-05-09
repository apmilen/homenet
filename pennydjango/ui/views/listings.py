from django.urls import reverse
from django.views.generic import DetailView

from ui.views.base_views import BaseContextMixin, PublicReactView

from rentals.models import RentProperty


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
        listings = [
            {
                'default_image': rp.default_image,
                'price': rp.price,
                'contact': rp.contact,
                'address': rp.address,
                'coords': ','.join(rp.coords),
                'about': rp.about,
                'bedrooms': rp.bedrooms,
                'baths': rp.baths,
                'pets_allowed': 'Yes' if rp.pets_allowed else 'No',
                'amenities': rp.amenities_list,
                'detail_link': reverse('listing_detail', args=[str(rp.id)]),
                'edit_link': reverse('admin:rentals_rentproperty_change', args=[str(rp.id)])
            } for rp in rent_properties
        ]

        return {
            'listings': listings
        }


class ListingDetail(BaseContextMixin, DetailView):
    model = RentProperty
    template_name = 'rentals/listing_detail.html'
