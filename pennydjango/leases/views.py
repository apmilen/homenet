from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic import CreateView

from rest_framework import viewsets

from penny.model_utils import get_all_or_by_user
from penny.mixins import ClientOrAgentRequiredMixin, AgentRequiredMixin
from penny.utils import ExtendedEncoder
from listings.mixins import ListingContextMixin
from listings.serializer import PrivateListingSerializer
from leases.models import Lease
from leases.form import LeaseCreateForm
from leases.serializer import LeaseSerializer
from ui.views.base_views import PublicReactView


# React
class LeaseDetail(ClientOrAgentRequiredMixin, PublicReactView):
    title = 'Lease Detail'
    component = 'pages/lease.js'
    pk_url_kwarg = 'pk'
    template = 'ui/react_base_card.html'

    def props(self, request, *args, **kwargs):
        queryset = Lease.objects.all()
        try:
            pk = self.kwargs.get(self.pk_url_kwarg)
            # Get the single item from the filtered queryset
            obj = queryset.get(pk=pk)
        except queryset.model.DoesNotExist:
            raise Http404(f"No {queryset.model._meta.verbose_name}s "
                          f"found matching the query")

        return {
            'lease': LeaseSerializer(obj).data,
        }


class LeasesList(AgentRequiredMixin, PublicReactView):
    title = 'Leases Management'
    component = 'pages/leases.js'
    template = 'ui/react_base_card.html'

    def props(self, request, *args, **kwargs):
        constants = {
        }

        return {
            'constants': constants,
            'endpoint': '/leases/private/'
        }


class LeaseCreate(AgentRequiredMixin,
                  ListingContextMixin,
                  PublicReactView,
                  CreateView):
    model = Lease
    form_class = LeaseCreateForm
    title = 'Create Offer'
    component = 'pages/listing.js'
    template = 'leases/create.html'
    template_name = 'leases/create.html'

    def get(self, request, *args, **kwargs):
        self.object = None

        props = self.get_props(request, *args, **kwargs)
        if request.GET.get('props_json'):
            return JsonResponse(props, encoder=ExtendedEncoder)

        context = self.get_context(request, *args, **kwargs)
        context['props'] = props
        context.update(**self.get_context_data())

        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('leases:detail', args=[self.object.id])

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.listing = self.get_listing()
        self.object.created_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def props(self, request, *args, **kwargs):
        return {
            'listing': PrivateListingSerializer(self.get_listing()).data,
        }


# Rest Framework
class LeaseViewSet(AgentRequiredMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Lease.objects.all()
    serializer_class = LeaseSerializer

    def get_queryset(self):
        self.queryset = super().get_queryset()
        user = self.request.user
        self.queryset = get_all_or_by_user(
            Lease,
            user,
            'created_by',
            self.queryset
        )
        return self.queryset.order_by('-modified')
