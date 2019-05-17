from django.views.generic import CreateView, TemplateView, DetailView

from penny.mixins import AgentRequiredMixin
from . import models as listing_models
from . import forms as listing_forms


class MainListingCreate(AgentRequiredMixin, CreateView):
    template_name = 'listings/create_main_listing.html'
    model = listing_models.Listing
    form_class = listing_forms.ListingForm
