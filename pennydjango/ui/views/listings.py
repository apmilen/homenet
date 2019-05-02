from django.views.generic import DetailView

from rentals.models import RentProperty
from .base_views import BaseContextMixin


class ListingDetail(BaseContextMixin, DetailView):
    model = RentProperty
    template_name = 'rentals/listing_detail.html'
