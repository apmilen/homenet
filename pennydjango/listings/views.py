from django.views.generic import CreateView

from .models import Listing
from .forms import ListingForm


class MainListingCreate(CreateView):
    template_name = 'listings/create_main_listing.html'
    model = Listing
    form_class = ListingForm

