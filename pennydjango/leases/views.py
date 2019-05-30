from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, CreateView

from penny.mixins import ClientOrAgentRequiredMixin
from listings.mixins import ListingContextMixin
from listings.models import Listing
from leases.models import Lease
from leases.form import LeaseCreateForm


class LeaseCreate(ClientOrAgentRequiredMixin, ListingContextMixin, CreateView):
    model = CreateView
    form_class = LeaseCreateForm
    template_name = 'leases/create.html'

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        lease = form.save(commit=False)
        lease.listing = self.listing
        lease.save()
        return HttpResponseRedirect(self.get_success_url())


class LeaseDetail(ClientOrAgentRequiredMixin, DetailView):
    model = Lease
