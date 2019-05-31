from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView
)

from rest_framework import viewsets

from penny.mixins import AgentRequiredMixin
from ui.views.base_views import BaseContextMixin, PublicReactView
from listings.forms import (
    ListingForm, ListingDetailForm, ListingPhotosForm, ListingPhotoFormSet
)
from listings.mixins import WizardMixin
from listings.models import Listing, ListingDetail, ListingPhotos, ListingPhoto
from listings.serializer import (
    PublicListingSerializer, PrivateListingSerializer
)
from listings.constants import (
    PETS_ALLOWED, AMENITIES, LISTING_TYPES, LISTING_STATUS
)
from listings.utils import filter_listings


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos_formset'] = ListingPhotoFormSet(
            queryset=ListingPhoto.objects.filter(listing_id=self.object.id)
        )
        return context

    def form_valid(self, form):
        photos_formset = ListingPhotoFormSet(
            self.request.POST, self.request.FILES
        )
        if photos_formset.is_valid():
            primary_photo = form.save()
            for photo_form in photos_formset:
                if photo_form.cleaned_data:
                    photo = photo_form.save(commit=False)
                    photo.listing = primary_photo
                    photo.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)


class ReviewListing(BaseContextMixin, WizardMixin, TemplateView):
    template_name = 'listings/review_listing.html'

    def get_listing_qs(self):
        self.listing_qs = super().get_listing_qs()
        self.listing_qs = self.listing_qs.select_related(
            'detail', 'photos', 'listing_agent', 'sales_agent'
        )
        return self.listing_qs


class Listings(AgentRequiredMixin, PublicReactView):
    title = 'Listings Management'
    component = 'pages/listings.js'

    def props(self, request, *args, **kwargs):
        constants = {
            'pets_allowed': dict(PETS_ALLOWED),
            'amenities': {
                amenity_tuple[0]: amenity_tuple[1]
                for _, group in dict(AMENITIES).items()
                for amenity_tuple in group
            },
            'listing_types': dict(LISTING_TYPES),
            'listing_status': dict(LISTING_STATUS),
        }

        return {
            'constants': constants,
            'endpoint': '/listings/private/'
        }


class ListingDetail(BaseContextMixin, DetailView):
    model = Listing
    template_name = 'listings/listing_detail.html'

    def get_queryset(self):
        return Listing.objects.select_related(
            'detail', 'photos', 'listing_agent',
        )


# ViewSets define the view behavior.
class PublicListingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Listing.objects.filter(
        status='approved',
        detail__private=False
    )
    serializer_class = PublicListingSerializer

    def get_queryset(self):
        queryset = filter_listings(self.queryset, self.request.query_params)

        # remember to use always the page param
        # http://localhost:8000/listings/public/?page=1&price_min=3000
        return queryset.order_by('-modified')


# ViewSets define the view behavior.
class PrivateListingViewSet(AgentRequiredMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = PrivateListingSerializer

    def get_queryset(self):
        queryset = filter_listings(self.queryset, self.request.query_params)
        return queryset.order_by('-modified')
