from django.http import Http404
from django.urls import reverse
from django.views.generic import (
    ListView, CreateView, UpdateView, DetailView, TemplateView
)

from rest_framework import viewsets

from penny.mixins import AgentRequiredMixin
from ui.views.base_views import BaseContextMixin
from listings.forms import ListingForm, ListingDetailForm, ListingPhotosForm
from listings.models import Listing, ListingDetail, ListingPhotos
from listings.serializer import ListingSerializer


class WizardMixin:
    pk_url_kwarg = 'pk'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listing = None
        self.listing_qs = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listing'] = self.get_listing()
        return context

    def get_object(self, queryset=None):
        self.listing = self.get_listing()
        queryset = self.get_queryset()
        obj, _ = queryset.get_or_create(listing=self.listing)
        return obj

    def get_listing_qs(self):
        self.listing_qs = Listing.objects.all()
        return self.listing_qs

    def get_listing(self):
        if self.listing:
            return self.listing

        queryset = self.get_listing_qs()
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
        return reverse("listings:review", kwargs={'pk': self.listing.id})


class ReviewListing(BaseContextMixin, WizardMixin, TemplateView):
    template_name = 'listings/review_listing.html'

    def get_listing_qs(self):
        self.listing_qs = super().get_listing_qs()
        self.listing_qs = self.listing_qs.select_related(
            'detail', 'photos', 'listing_agent', 'sales_agent'
        )
        return self.listing_qs


class Listings(AgentRequiredMixin, ListView):
    def get_queryset(self):
        return Listing.objects.order_by('-modified').all()


class ListingDetail(BaseContextMixin, DetailView):
    model = Listing
    template_name = 'listings/listing_detail.html'

    def get_queryset(self):
        return Listing.objects.select_related(
            'detail', 'photos', 'listing_agent',
        )


# ViewSets define the view behavior.
class PublicListingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            status='approved',
            detail__private=False
        )
        # We can filter here with self.request.query_params
        # https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-query-parameters
        print(self.request.query_params)

        pets_allowed = self.request.query_params.get('pets_allowed')
        if pets_allowed != 'any':
            queryset = queryset.filter(pets=pets_allowed)

        # remember to use always the page param
        # http://localhost:8000/listings/public/?page=1&price_min=3000
        return queryset.order_by('-created')
