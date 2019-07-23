from django.urls import reverse
from django.http import Http404
from django.views.generic import ListView, DeleteView

from penny.mixins import AgentRequiredMixin
from listing_collections.models import Collection


class CollectionsList(AgentRequiredMixin, ListView):
    model = Collection
    template_name = 'listing_collections/collections.html'

    def get_queryset(self):
        return Collection.objects.filter(created_by=self.request.user)


class CollectionDelete(AgentRequiredMixin, DeleteView):
    model = Collection

    def get_success_url(self):
        return reverse('collections:list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.created_by == self.request.user:
            raise Http404
        return obj
