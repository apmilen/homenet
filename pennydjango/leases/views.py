from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction, DatabaseError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import CreateView, DetailView, TemplateView, \
    RedirectView

from rest_framework import viewsets

from datatables_listview.core.views import DatatablesListView
from leases.emails import send_invitation_email
from leases.form import LeaseCreateForm, BasicLeaseMemberForm, MoveInCostForm
from leases.models import Lease, LeaseMember, MoveInCost
from leases.serializer import LeaseSerializer
from listings.mixins import ListingContextMixin
from listings.models import Listing
from listings.serializer import PrivateListingSerializer
from penny.constants import CLIENT_TYPE
from penny.forms import CustomUserCreationForm
from penny.mixins import (
    ClientOrAgentRequiredMixin, AgentRequiredMixin, MainObjectContextMixin
)
from penny.model_utils import get_all_or_by_user
from penny.models import User
from penny.utils import ExtendedEncoder
from ui.views.base_views import PublicReactView


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


# React
class LeaseDetail(ClientOrAgentRequiredMixin, DetailView):
    model = Lease
    template_name = 'leases/lease_agent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lease_members = self.object.leasemember_set.select_related('user')
        move_in_costs = self.object.moveincost_set.order_by('-created')
        context['listing'] = self.object.listing
        context['lease_members'] = lease_members
        context['move_in_costs'] = move_in_costs
        context['invite_member_form'] = BasicLeaseMemberForm()
        context['move_in_costs_form'] = MoveInCostForm(pk=self.object.id)
        context['total'] = MoveInCost.objects.total_by_offer(self.object.id)
        return context


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
        self.object.listing = self.get_main_object()
        self.object.created_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def props(self, request, *args, **kwargs):
        return {
            'listing': PrivateListingSerializer(self.get_main_object()).data,
        }


# Django
class LeaseMemberCreate(MainObjectContextMixin, AgentRequiredMixin, CreateView):
    http_method_names = ['post']
    model = LeaseMember
    main_model = Lease
    form_class = BasicLeaseMemberForm

    def get_success_url(self):
        return reverse('leases:detail', args=[self.main_object.id])

    def form_valid(self, form):
        try:
            with transaction.atomic():
                member = form.save(commit=False)
                member.offer = self.get_main_object()
                member.save()
                send_invitation_email(member)
        except DatabaseError:
            messages.add_message(
                self.request,
                messages.ERROR,
                "An error has occurred"
            )
            return self.form_invalid(form)

        return HttpResponseRedirect(self.get_success_url())


class MoveInCostCreate(MainObjectContextMixin, AgentRequiredMixin, CreateView):
    http_method_names = ['post']
    model = MoveInCost
    main_model = Lease
    form_class = MoveInCostForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'pk': self.main_object.id})
        return kwargs

    def form_valid(self, form):
        cost = form.save(commit=False)
        lease = self.get_main_object()
        cost.offer = lease
        cost.save()
        total = MoveInCost.objects.total_by_offer(lease.id)
        return JsonResponse(data={
            'status': 200,
            'total': total,
            'value': render_to_string('leases/move_in_cost.html', context={
                'charge': cost.charge,
                'value': cost.value
            })
        })

    def form_invalid(self, form):
        return JsonResponse(data={'status': 500, 'errors': form.errors})


class LeaseClientCreate(MainObjectContextMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    main_model = LeaseMember
    template_name = 'leases/create_client.html'

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Account created successfully"
        )
        return reverse('home')

    def get(self, request, *args, **kwargs):
        self.main_object = self.get_main_object()
        if self.main_object.user:
            messages.add_message(
                self.request,
                messages.INFO,
                "You have already accepted the invitation. Log in to your "
                "account to access your current lease"
            )
            return redirect(reverse('home'))
        return super().get(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        lease_member = self.get_main_object()
        initial.update({
            'email': lease_member.email,
            'first_name': lease_member.name
        })
        return initial

    def form_valid(self, form):
        try:
            with transaction.atomic():
                new_user = form.save(commit=False)
                new_user.user_type = CLIENT_TYPE
                new_user.save()
                self.main_object.user = new_user
                self.main_object.save()
        except DatabaseError:
            messages.add_message(
                self.request,
                messages.ERROR,
                "An error has occurred while creating the user"
            )
            return self.form_invalid(form)
        login(self.request, new_user)

        return HttpResponseRedirect(self.get_success_url())


# class ClientLeasesList(LoginRequiredMixin, DatatablesListView, TemplateView):
#     model = Listing
#     template_name = 'penny/user_settings/_datatables_base.html'
#     fields = ('address', 'term', 'price')
#     column_names_and_defs = ('Address', 'Term', 'Rent')
#     table_name = 'Lease History'
#     options_list = [
#         {
#             'option_label': 'Enter',
#             'option_url': 'penny:user_settings',
#             'url_params': [],
#             'icon': 'user'
#         }
#     ]
#
#     def get_queryset(self):
#         user = self.request.user
#         lookup = ["offer__listing__id", "offer__move_in_date"]
#         lease_members = LeaseMember.objects.only(*lookup).filter(user=user)
#         id_list = lease_members.values_list("offer__listing__id", flat=True)
#         return self.model.objects.filter(id__in=id_list)


class ClientLeasesList(LoginRequiredMixin, TemplateView):
    model = Listing
    template_name = 'penny/_aux_lease_dt.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        lookup = ["offer_id",
                  "offer__listing__address",
                  "offer__listing__term",
                  "offer__listing__price",
                  "offer__move_in_date"]
        lease_members = LeaseMember.objects.only(*lookup).filter(user=user)
        context.update({"rows": lease_members})
        context['normal'] = True
        return context


class ResendLeaseInvitation(ClientOrAgentRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Invitations sent"
        )
        pk = kwargs.get('lease_id')
        return reverse("leases:detail", args=[pk])

    def get(self, request, *args, **kwargs):
        lease_member = get_object_or_404(LeaseMember, id=kwargs.get('pk'))
        send_invitation_email(lease_member)
        kwargs.update({"lease_id": lease_member.offer_id})
        return super().get(request, *args, **kwargs)


class ClientLease(ClientOrAgentRequiredMixin, DetailView):
    model = Lease
    template_name = 'leases/client_lease.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lease_members = self.object.leasemember_set.select_related('user')
        move_in_costs = self.object.moveincost_set.order_by('-created')
        context['listing'] = self.object.listing
        context['lease_members'] = lease_members
        context['move_in_costs'] = move_in_costs
        context['invite_member_form'] = BasicLeaseMemberForm()
        context['total'] = MoveInCost.objects.total_by_offer(self.object.id)
        return context

