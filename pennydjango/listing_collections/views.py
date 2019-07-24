from django.conf import settings
from django.urls import reverse
from django.http import Http404
from django.views.generic import ListView, DeleteView, DetailView

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


class CollectionDetail(DetailView):
    model = Collection
    template_name = 'listing_collections/collection_detail.html'
    slug_field = 'id__startswith'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['map_key'] = settings.MAP_KEY
        return context
