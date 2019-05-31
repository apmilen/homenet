from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView

from rest_framework import viewsets

from penny.model_utils import get_all_or_by_user
from penny.mixins import ClientOrAgentRequiredMixin, AgentRequiredMixin
from listings.mixins import ListingContextMixin
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


class LeaseDetail(ClientOrAgentRequiredMixin, PublicReactView):
    title = 'Lease Detail'
    component = 'pages/lease.js'
    pk_url_kwarg = 'pk'

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
