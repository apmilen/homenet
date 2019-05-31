from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, CreateView, ListView

from rest_framework import viewsets

from penny.model_utils import get_all_or_by_user
from penny.mixins import ClientOrAgentRequiredMixin, AgentRequiredMixin
from listings.mixins import ListingContextMixin
from listings.models import Listing
from leases.models import Lease
from leases.form import LeaseCreateForm
from leases.serializer import LeaseSerializer
from ui.views.base_views import PublicReactView


class LeasesList(AgentRequiredMixin, PublicReactView):
    title = 'Leases Management'
    component = 'pages/leases.js'

    def props(self, request, *args, **kwargs):
        constants = {
        }

        return {
            'constants': constants,
            'endpoint': '/leases/private/'
        }


class LeaseCreate(AgentRequiredMixin, ListingContextMixin, CreateView):
    model = Lease
    form_class = LeaseCreateForm
    template_name = 'leases/create.html'

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        lease = form.save(commit=False)
        lease.listing = self.get_listing()
        lease.created_by = self.request.user
        lease.save()
        return HttpResponseRedirect(self.get_success_url())


class LeaseDetail(ClientOrAgentRequiredMixin, DetailView):
    model = Lease


# ViewSets define the view behavior.
class LeaseViewSet(AgentRequiredMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Lease.objects.all()
    serializer_class = LeaseSerializer

    def get_queryset(self):
        self.queryset = super().get_queryset()
        user = self.request.user
        self.queryset = get_all_or_by_user(
            None,
            user,
            'created_by',
            self.queryset
        )
        return self.queryset.order_by('-modified')