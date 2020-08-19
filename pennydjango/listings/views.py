import os

from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView
)

from rest_framework import viewsets

from penny.models import User
from penny.mixins import AgentRequiredMixin
from penny.utils import ExtendedEncoder
from penny.constants import NEIGHBORHOODS, AGENT_TYPE
from ui.views.base_views import BaseContextMixin, PublicReactView
from listings.forms import (
    ListingForm, ListingDetailForm, ListingPhotosForm, SingleListingPhotoForm,
    ChangeListingStatusForm
)
from listings.mixins import WizardMixin
from listings.models import Listing, ListingDetail, ListingPhotos, ListingPhoto
from listings.serializer import (
    PublicListingSerializer, PrivateListingSerializer
)
from listings.constants import (
    PETS_ALLOWED, AMENITIES, LISTING_TYPES, TRANSIT_OPTIONS
)
from listings.utils import qs_from_filters, get_query_params_as_object


# ViewSets define the view behavior.
class PublicListingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Listing.objects.filter(
        status='approved',
        detail__private=False
    )
    serializer_class = PublicListingSerializer

    def get_queryset(self):
        queryset = qs_from_filters(self.queryset, self.request.query_params)

        # remember to use always the page param
        # http://localhost:8000/listings/public/?page=1&price_min=3000
        return queryset.order_by('-modified')


# ViewSets define the view behavior.
class PrivateListingViewSet(AgentRequiredMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = PrivateListingSerializer

    def get_queryset(self):
        queryset = qs_from_filters(self.queryset, self.request.query_params)
        return queryset.order_by('-modified')


class MainListingCreate(AgentRequiredMixin, CreateView):
    template_name = 'listings/main_listing.html'
    model = Listing
    form_class = ListingForm

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()
            primary_photo = ListingPhotos(listing=self.object)
            detail = ListingDetail(listing=self.object)
            primary_photo.save()
            detail.save()
        return HttpResponseRedirect(self.get_success_url())

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

    def form_valid(self, form):
        instance = form.save()
        instance.listing.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("listings:photos", kwargs={'pk': self.listing.id})


class PhotosListingUpdate(AgentRequiredMixin, WizardMixin, UpdateView):
    template_name = 'listings/photos_listing.html'
    model = ListingPhotos
    form_class = ListingPhotosForm
    http_method_names = ['get']

    def get_success_url(self):
        return reverse("listings:review", kwargs={'pk': self.listing.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = self.object.listingphoto_set.all()
        return context


class UploadPrimaryPhoto(AgentRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            listing_photo = ListingPhotos.objects.get(
                listing_id=kwargs.get('pk')
            )
            # Save the previous path to delete later
            delete_path = None
            if listing_photo.primary_photo:
                delete_path = listing_photo.primary_photo.path

            form = ListingPhotosForm(
                None,
                request.FILES,
                instance=listing_photo
            )
            instance = form.save()
            instance.listing.save()
            # delete old image form disk
            if delete_path:
                try:
                    os.remove(delete_path)
                except FileNotFoundError:
                    pass
            return JsonResponse({'status': 200})
        # Bad request
        return JsonResponse({'status': 401})


class UploadExtraPhoto(AgentRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            listing_photo = ListingPhotos.objects.get(
                listing_id=kwargs.get('pk')
            )
            form = SingleListingPhotoForm(
                None,
                request.FILES,
            )
            photo = form.save(commit=False)
            photo.listing = listing_photo
            photo.save()
            listing_photo.listing.save()
            return JsonResponse({'status': 200})
        # Bad request
        return JsonResponse({'status': 401})


class DeleteExtraPhoto(AgentRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        listing_photo = get_object_or_404(ListingPhoto, id=kwargs.get('pk'))
        delete_path = None
        if listing_photo.photo:
            delete_path = listing_photo.photo.path
        listing_photo.delete()
        # delete old image form disk
        if delete_path:
            try:
                os.remove(delete_path)
            except FileNotFoundError:
                pass
        return HttpResponseRedirect(
            reverse('listings:photos', args=[listing_photo.listing.listing.id])
        )


class ReviewListing(WizardMixin, PublicReactView, TemplateView):
    template = 'listings/review_listing.html'
    component = 'pages/listing.js'

    def get_template_names(self):
        return [self.template]

    def get_main_object_qs(self):
        self.main_object_qs = super().get_main_object_qs()
        self.main_object_qs = self.main_object_qs.select_related(
            'detail', 'photos', 'listing_agent'
        )
        return self.main_object_qs

    def get(self, request, *args, **kwargs):
        props = self.get_props(request, *args, **kwargs)
        if request.GET.get('props_json'):
            return JsonResponse(props, encoder=ExtendedEncoder)

        context = self.get_context(request, *args, **kwargs)
        context['props'] = props
        context.update(**self.get_context_data())

        return self.render_to_response(context)

    def props(self, request, *args, **kwargs):
        return {
            'listing': PrivateListingSerializer(self.get_main_object()).data,
        }


class ListingDetailView(BaseContextMixin, DetailView):
    model = Listing
    template_name = 'listings/listing_detail.html'

    def get_queryset(self):
        return Listing.objects.select_related(
            'detail', 'photos', 'listing_agent',
        )

    def context(self, request, *args, **kwargs):
        user = self.request.user
        context = {'map_key': settings.MAPBOX_API_KEY}
        if user.is_authenticated and user.perms.has_agent_access:
            context['change_status_form'] = ChangeListingStatusForm(
                instance=self.object
            )
        return context


class ChangeListingStatusView(AgentRequiredMixin, UpdateView):
    model = Listing
    form_class = ChangeListingStatusForm

    def get_success_url(self):
        return reverse("listings:listings")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Listing updated"
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(
            self.request,
            messages.ERROR,
            "An error has occurred while updating the Listing"
        )
        return HttpResponseRedirect(self.get_success_url())


class Listings(AgentRequiredMixin, PublicReactView):
    title = 'Listings Management'
    component = 'pages/listings.js'

    def props(self, request, *args, **kwargs):
        query_filters = get_query_params_as_object(request.GET)
        constants = {
            'pets_allowed': dict(PETS_ALLOWED),
            'amenities': {
                amenity_tuple[0]: amenity_tuple[1]
                for _, group in dict(AMENITIES).items()
                for amenity_tuple in group
            },
            'listing_types': dict(LISTING_TYPES),
            'neighborhoods': dict(NEIGHBORHOODS),
            'nearby_transit': dict(TRANSIT_OPTIONS),
            'agents': [
                (agent.username, agent.get_full_name(), agent.avatar_url)
                for agent in User.objects.filter(user_type=AGENT_TYPE)
            ],
        }
        return {
            'constants': constants,
            'initial_filters': query_filters,
            'endpoint': '/listings/private/'
        }

    def post(self, request, *args, **kwargs):
        req_type = request.POST.get('type')
        response = {'status': 400, 'success': False}
        if req_type == 'LISTING_COLLECTION':
            collection_id = request.POST.get('collection_id')
            listing_id = request.POST.get('listing_id')
            assert collection_id and listing_id

            listing = Listing.objects.get(id=listing_id)
            listing_in_collection = listing.collections\
                .filter(id=collection_id).exists()

            if listing_in_collection:
                listing.collections.remove(collection_id)
            else:
                listing.collections.add(collection_id)

            listing_data = PrivateListingSerializer(listing).data
            response = {
                'status': 200,
                'success': True,
                'collections': listing_data['collections']
            }

        if req_type == 'CREATE_COLLECTION':
            name = request.POST.get('name')
            notes = request.POST.get('notes')
            listing_id = request.POST.get('listing_id')

            if not (name and notes and listing_id):
                response = {
                    'status': 400,
                    'success': False,
                    'errors': ["Missing data"],
                }
            else:
                listing = Listing.objects.get(id=listing_id)
                listing.collections.create(
                    name=name,
                    notes=notes,
                    created_by=request.user
                )
                response = {'status': 200, 'success': True}

        return JsonResponse(response)
