from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, CreateView, ListView

from penny.model_utils import get_all_or_by_user
from penny.mixins import ClientOrAgentRequiredMixin, AgentRequiredMixin
from listings.mixins import ListingContextMixin
from listings.models import Listing
from leases.models import Lease
from leases.form import LeaseCreateForm


class LeasesList(AgentRequiredMixin, ListView):
    model = Lease

    def get_queryset(self):
        user = self.request.user
        self.queryset = get_all_or_by_user(self.model, user, 'created_by')
        return self.queryset


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
