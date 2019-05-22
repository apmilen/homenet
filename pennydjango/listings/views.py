from django.http import Http404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DetailView

from penny.mixins import AgentRequiredMixin
from ui.views.base_views import BaseContextMixin, PublicReactView
from listings.models import Listing, ListingDetail, ListingPhotos
from listings.forms import ListingForm, ListingDetailForm, ListingPhotosForm
from listings.constants import APPROVED


class WizardMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listing = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listing'] = self.listing
        return context

    def get_object(self, queryset=None):
        self.listing = self.get_listing()
        queryset = self.get_queryset()
        obj, _ = queryset.get_or_create(listing=self.listing)
        return obj

    def get_listing(self):
        if self.listing:
            return self.listing

        queryset = Listing.objects.all()
        try:
            pk = self.kwargs.get(self.pk_url_kwarg)
            # Get the single item from the filtered queryset
            obj = queryset.get(pk=pk)
        except queryset.model.DoesNotExist:
            raise Http404(f"No {queryset.model._meta.verbose_name}s "
                          f"found matching the query")
        return obj


class MainListingCreate(AgentRequiredMixin, CreateView):
    template_name = 'listings/main_listing.html'
    model = Listing
    form_class = ListingForm

    def get_success_url(self):
        return reverse("listings:detail", kwargs={'pk': self.object.id})


class MainListingUpdate(AgentRequiredMixin, UpdateView):
    template_name = 'listings/main_listing.html'
    model = Listing
    form_class = ListingForm

    def get_success_url(self):
        return reverse("listings:detail", kwargs={'pk': self.object.id})


class DetailListingUpdate(AgentRequiredMixin, WizardMixin, UpdateView):
    template_name = 'listings/detail_listing.html'
    model = ListingDetail
    form_class = ListingDetailForm

    def get_success_url(self):
        return reverse("listings:photos", kwargs={'pk': self.listing.id})


class PhotosListingUpdate(AgentRequiredMixin, WizardMixin, UpdateView):
    template_name = 'listings/photos_listing.html'
    model = ListingPhotos
    form_class = ListingPhotosForm

    def get_success_url(self):
        # return reverse("listings:review", kwargs={'pk': self.listing.id})
        return reverse("home")


class Listings(PublicReactView):
    title = "Listings"
    component = 'pages/listings.js'

    def props(self, request, *args, **kwargs):
        query_filter = {'status': APPROVED}
        listings = Listing.objects.filter(**query_filter)

        return {
            'listings': [listing.__json__() for listing in listings]
        }


class ListingDetail(BaseContextMixin, DetailView):
    model = Listing
    template_name = 'listings/listing_detail.html'

    def get_queryset(self):
        return Listing.objects.select_related(
            'detail', 'photos', 'listing_agent',
        )
