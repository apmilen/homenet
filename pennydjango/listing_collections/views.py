from django.conf import settings
from django.urls import reverse
from django.http import Http404, JsonResponse, HttpResponseForbidden
from django.core.mail import send_mail
from django.views.generic import ListView, DeleteView, DetailView
from django.template.loader import render_to_string

from penny.mixins import AgentRequiredMixin
from listing_collections.models import Collection


class CollectionsList(AgentRequiredMixin, ListView):
    model = Collection
    template_name = 'listing_collections/collections.html'

    def get_queryset(self):
        return Collection.objects.filter(
            created_by=self.request.user
        ).order_by('-modified')


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
        context['map_key'] = settings.GOOGLE_MAPS_API_KEY
        return context

    def post(self, request, *args, **kwargs):
        # Collections are visible for non-logged users,
        # but they are not allowed to send emails
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        to_email = request.POST.get('email', '')
        note = request.POST.get('note', '')

        minimum_validation = all(
            required_char in to_email for required_char in ("@", ".")
        )
        if not minimum_validation:
            return JsonResponse({
                'status': 200,
                'success': False,
                'message': "Invalid email address"
            })

        collection = self.get_object()
        path = reverse('collections:detail', args=[collection.short_id])

        subject = f"Listing collection: {collection.name}"
        body = render_to_string(
            "email/collections/share_collection_link.txt",
            context={
                'url': f"{settings.BASE_URL}{path}",
                'note': note
            }
        )
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [to_email])

        return JsonResponse({
            'status': 200,
            'success': True,
            'message': "Email sent successfully"
        })
