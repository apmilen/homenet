from io import BytesIO
import os
import zipfile

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction, DatabaseError
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, RedirectView,
    DeleteView)
from django.views.generic.base import View
from django.utils.text import slugify

from rest_framework import viewsets
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration

from leases.emails import send_invitation_email
from leases.forms import (
    LeaseCreateForm, BasicLeaseMemberForm, MoveInCostForm, SignAgreementForm,
    RentalApplicationForm,
    RentalAppDocForm, ChangeLeaseStatusForm, RentalApplicationEditingForm)
from leases.mixins import ClientLeaseAccessMixin
from leases.models import Lease, LeaseMember, MoveInCost, RentalApplication, \
    RentalAppDocument
from leases.serializer import LeaseSerializer
from leases.utils import qs_from_filters
from leases.constants import LEASE_STATUS

from listings.mixins import ListingContextMixin
from listings.serializer import PrivateListingSerializer

from payments.models import Transaction
from payments.constants import CLIENT_TO_APP, APP_TO_CLIENT

from penny.mixins import (
    ClientOrAgentRequiredMixin, AgentRequiredMixin, MainObjectContextMixin
)
from penny.constants import NEIGHBORHOODS, AGENT_TYPE, CLIENT_TYPE
from penny.forms import CustomUserCreationForm
from penny.model_utils import get_all_or_by_user
from penny.models import User
from penny.utils import ExtendedEncoder, get_client_ip

from ui.views.base_views import PublicReactView

from django.db.models import Sum


# Rest Framework
class LeaseViewSet(AgentRequiredMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Lease.objects.all()
    serializer_class = LeaseSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = get_all_or_by_user(
            Lease,
            user,
            'created_by',
            self.queryset
        )
        queryset = qs_from_filters(queryset, self.request.query_params)
        return queryset.order_by('-modified')


# React
class LeaseDetail(AgentRequiredMixin, DetailView):
    model = Lease
    template_name = 'leases/lease_agent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lease_members = self.object.leasemember_set.select_related('user')
        move_in_costs = self.object.moveincost_set.order_by('-created')
        change_status_url = reverse('leases:change-status',
                                    args=[self.object.id])
        lease_transactions = Transaction.objects.filter(
            lease_member__offer=self.object
        )
        lease_postive_balance = lease_transactions.filter(
            from_to=CLIENT_TO_APP
        ).aggregate(Sum('amount'))
        lease_negative_balance = lease_transactions.filter(
            from_to=APP_TO_CLIENT
        ).aggregate(Sum('amount'))
        lease_postive_balance = lease_postive_balance['amount__sum'] or 0
        lease_negative_balance = lease_negative_balance['amount__sum'] or 0
        current_balance = lease_postive_balance - lease_negative_balance
        context['listing'] = self.object.listing
        context['lease_members'] = lease_members
        context['move_in_costs'] = move_in_costs
        context['invite_member_form'] = BasicLeaseMemberForm()
        context['change_status_form'] = ChangeLeaseStatusForm(
            instance=self.object
        )
        context['change_status_url'] = change_status_url
        context['move_in_costs_form'] = MoveInCostForm(pk=self.object.id)
        context['total'] = MoveInCost.objects.total_by_offer(self.object.id)
        context['lease_transactions'] = lease_transactions
        context['number_of_transactions'] = lease_transactions.count()
        context['current_balance'] = current_balance

        return context


class LeasesList(AgentRequiredMixin, PublicReactView):
    title = 'Leases Management'
    component = 'pages/leases.js'

    def props(self, request, *args, **kwargs):
        constants = {
            'lease_status': list(LEASE_STATUS),
            'neighborhoods': dict(NEIGHBORHOODS),
            'agents': [
                (agent.username, agent.get_full_name(), agent.avatar_url)
                for agent in User.objects.filter(user_type=AGENT_TYPE)
            ],
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


class LeaseUpdateView(AgentRequiredMixin, UpdateView):
    model = Lease
    form_class = LeaseCreateForm
    template_name = 'leases/lease_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listing'] = self.object.listing
        return context

    def get_success_url(self):
        messages.success(self.request, "Leases updated successfully")
        return self.object.detail_link()


# Django
class LeaseMemberCreate(MainObjectContextMixin,
                        ClientOrAgentRequiredMixin,
                        ClientLeaseAccessMixin,
                        CreateView):
    http_method_names = ['post']
    model = LeaseMember
    main_model = Lease
    form_class = BasicLeaseMemberForm
    get_object = 'get_main_object'

    def my_test_func(self):
        user = self.request.user
        if user.is_user_client:
            main_object = self.get_main_object()
            qs = LeaseMember.objects.filter(user=user, offer_id=main_object.id)
            return qs.exists()
        return True

    def get_success_url(self):
        if self.request.user.is_user_client:
            leasemember = LeaseMember.objects.only('id').get(
                user=self.request.user.id,
                offer_id=self.main_object.id
            )
            return reverse('leases:detail-client', args=[leasemember.id])
        else:
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

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.add_message(
            self.request,
            messages.ERROR,
            "An error has occurred while creating the user"
        )
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
    message = 'created'

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f"Account {self.message} successfully"
        )
        return self.main_object.client_detail_link()

    def not_logged_url(self):
        messages.add_message(
            self.request,
            messages.ERROR,
            "You must log in with the account linked to the email to accept."
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
        try:
            user = User.objects.get(email__iexact=self.main_object.email)
            if not user.id == self.request.user.id:
                return HttpResponseRedirect(self.not_logged_url())
            self.main_object.user = user
            self.main_object.save()
            self.message = 'linked'
        except User.DoesNotExist:
            print(self.main_object.email, flush=True)
        else:
            return HttpResponseRedirect(self.get_success_url())
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
    template_name = 'penny/_aux_lease_dt.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        lookup = ["offer__listing__address",
                  "offer__listing__term",
                  "offer__listing__price",
                  "offer__move_in_date"]
        lease_members = LeaseMember.objects.only(*lookup).filter(user=user)
        context.update({"rows": lease_members})
        context['normal'] = True
        return context


class ResendLeaseInvitation(ClientOrAgentRequiredMixin,
                            ClientLeaseAccessMixin,
                            RedirectView):
    object = None

    def my_test_func(self):
        user = self.request.user
        if user.is_user_client:
            main_object_id = self.get_object().offer_id
            qs = LeaseMember.objects.filter(user=user, offer_id=main_object_id)
            return qs.exists()
        return True

    def get_object(self):
        if self.object:
            return self.object
        self.object = get_object_or_404(LeaseMember, id=self.kwargs.get('pk'))
        return self.object

    def get_redirect_url(self, *args, **kwargs):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Invitations sent"
        )
        if self.request.user.is_user_client:
            leasemember = LeaseMember.objects.only('id').get(
                user=self.request.user.id,
                offer_id=self.object.offer.id
            )
            return reverse('leases:detail-client', args=[leasemember.id])
        else:
            return reverse('leases:detail', args=[self.object.offer.id])

    def get(self, request, *args, **kwargs):
        lease_member = self.get_object()
        send_invitation_email(lease_member)
        kwargs.update({"lease_id": lease_member.offer_id})
        return super().get(request, *args, **kwargs)


class ClientLease(ClientOrAgentRequiredMixin,
                  ClientLeaseAccessMixin,
                  DetailView):
    model = LeaseMember
    template_name = 'leases/client_lease.html'

    def get_queryset(self, queryset=None):
        return self.model.objects.select_related('offer', 'offer__listing')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Main objects
        lease = self.object.offer
        rental_app, _ = RentalApplication.objects.get_or_create(
            lease_member=self.object
        )
        lease_members = lease.leasemember_set.select_related('user')
        move_in_costs = lease.moveincost_set.order_by('-created')
        lease_transactions = Transaction.objects.filter(lease_member__offer=lease)
        total_paid_lease = lease_transactions.aggregate(Sum('amount'))
        total_move_in_cost = MoveInCost.objects.total_by_offer(lease.id)
        lease_pending_payment = total_move_in_cost
        if total_paid_lease['amount__sum'] is not None:
            lease_pending_payment = total_move_in_cost - total_paid_lease['amount__sum']           
        # Context
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        context['lease'] = lease
        context['listing'] = lease.listing
        context['rental_app'] = rental_app
        context['lease_members'] = lease_members
        context['move_in_costs'] = move_in_costs
        context['total'] = total_move_in_cost
        context['invite_member_form'] = BasicLeaseMemberForm()
        context['agreement_form'] = SignAgreementForm()
        context['lease_transactions'] = lease_transactions
        context['lease_pending_payment'] = lease_pending_payment
        
        # Application context
        if not rental_app.completed or rental_app.editing:
            context['rental_application_form'] = RentalApplicationForm(
                instance=rental_app
            )
            context['rental_docs'] = rental_app.rentalappdocument_set.all()
        return context


class SignAgreementView(ClientOrAgentRequiredMixin,
                        ClientLeaseAccessMixin,
                        UpdateView):
    http_method_names = ('post', )
    model = LeaseMember
    form_class = SignAgreementForm

    def get_success_url(self):
        return reverse('leases:detail-client', args=[self.object.id])

    def form_valid(self, form):
        member = form.save(commit=False)
        ip_address = get_client_ip(self.request)
        user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        member.signed_agreement = timezone.now()
        member.ip_address = ip_address
        member.user_agent = user_agent
        member.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return HttpResponseRedirect(self.get_success_url())


class DeleteLeaseMember(ClientOrAgentRequiredMixin,
                        ClientLeaseAccessMixin,
                        DeleteView):
    http_method_names = ['post']
    model = LeaseMember

    def my_test_func(self):
        user = self.request.user
        if user.is_user_client:
            main_object_id = self.get_object().offer_id
            qs = LeaseMember.objects.filter(user=user, offer_id=main_object_id)
            return qs.exists()
        return True

    def get_success_url(self):
        if self.request.user.is_user_client:
            leasemember = LeaseMember.objects.only('id').get(
                user=self.request.user.id,
                offer_id=self.object.offer.id
            )
            return reverse('leases:detail-client', args=[leasemember.id])
        else:
            return reverse('leases:detail', args=[self.object.offer.id])

    def delete(self, request, *args, **kwargs):
        self.object = super().get_object()
        if self.object.user:
            messages.add_message(
                self.request,
                messages.ERROR,
                "Cannot delete a lease member with a created account"
            )
            return HttpResponseRedirect(self.get_success_url())
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


class UpdateRentalApplication(ClientOrAgentRequiredMixin,
                              ClientLeaseAccessMixin,
                              UpdateView):
    http_method_names = ['post']
    form_class = RentalApplicationForm
    model = RentalApplication
    direct = False

    def get_success_url(self):
        leasemember_id = self.object.lease_member.id
        return reverse("leases:detail-client", args=[leasemember_id])

    def form_valid(self, form):
        completed = self.request.GET.get('completed') == "true"
        rental_app = form.save(commit=False)
        rental_app.completed = completed
        rental_app.editing = not completed
        rental_app.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return HttpResponseRedirect(self.get_success_url())


class UpdateEditingRentalApplication(ClientOrAgentRequiredMixin,
                                     ClientLeaseAccessMixin,
                                     UpdateView):
    http_method_names = ['post']
    form_class = RentalApplicationEditingForm
    model = RentalApplication
    direct = False

    def get_success_url(self):
        leasemember_id = self.object.lease_member.id
        return reverse("leases:detail-client", args=[leasemember_id])

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return HttpResponseRedirect(self.get_success_url())


class UploadRentalAppDoc(ClientOrAgentRequiredMixin,
                         ClientLeaseAccessMixin,
                         View):
    http_method_names = ['post']
    direct = False

    def get_object(self):
        if self.object:
            return self.object
        self.object = get_object_or_404(
            RentalApplication, id=self.kwargs.get('pk')
        )
        return self.object

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            rental_app = self.get_object()
            form = RentalAppDocForm(
                None,
                request.FILES,
            )
            doc = form.save(commit=False)
            doc.rental_app = rental_app
            doc.save()
            return JsonResponse({'status': 200})
        # Bad request
        return JsonResponse({'status': 401})


class DeleteRentalAppDoc(ClientOrAgentRequiredMixin,
                         ClientLeaseAccessMixin,
                         View):
    http_method_names = ['get']
    direct = False

    def get_lease_member(self, test_object):
        return test_object.rental_app.lease_member

    def get_object(self):
        if self.object:
            return self.object
        self.object = get_object_or_404(
            RentalAppDocument, id=self.kwargs.get('pk')
        )
        return self.object

    def get(self, request, *args, **kwargs):
        rental_doc = self.get_object()
        lease_member_id = rental_doc.rental_app.lease_member.id
        delete_path = None
        if rental_doc.file:
            delete_path = rental_doc.file.path
        rental_doc.delete()
        # delete old image form disk
        if delete_path:
            try:
                os.remove(delete_path)
            except FileNotFoundError:
                pass
        messages.success(self.request, "Document deleted")
        return HttpResponseRedirect(
            reverse('leases:detail-client', args=[lease_member_id])
        )


class RentalApplicationDetail(ClientOrAgentRequiredMixin,
                              ClientLeaseAccessMixin,
                              DetailView):
    model = RentalApplication
    template_name = 'leases/rental_app/rental_app_detail.html'
    direct = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lease_member'] = self.object.lease_member
        context['rental_docs'] = self.object.rentalappdocument_set.all()
        return context


class DownloadRentalDocuments(ClientOrAgentRequiredMixin,
                              ClientLeaseAccessMixin,
                              View):
    direct = False

    def get_object(self):
        if self.object:
            return self.object
        self.object = get_object_or_404(
            RentalApplication, id=self.kwargs.get('pk')
        )
        return self.object

    def get(self, *args, **kwargs):
        rental_app = self.get_object()
        lease_member = rental_app.lease_member
        zip_subdir = f'{lease_member.get_full_name()}'
        zip_filename = f'{zip_subdir}.zip'

        bytes_io = BytesIO()
        zipf = zipfile.ZipFile(bytes_io, "w")

        for doc in rental_app.rentalappdocument_set.all():
            fdir, fname = os.path.split(doc.file.path)
            zip_path = os.path.join(zip_subdir, fname)
            zipf.write(doc.file.path, zip_path)

        zipf.close()

        response = HttpResponse(
            bytes_io.getvalue(),
            content_type="application/x-zip-compressed"
        )

        response['Content-Disposition'] = f'attachment; filename={zip_filename}'
        return response


class ChangeLeaseStatusView(AgentRequiredMixin, UpdateView):
    model = Lease
    form_class = ChangeLeaseStatusForm

    def get_success_url(self):
        return self.object.detail_link()

    def form_valid(self, form):
        messages.success(
            self.request,
            "Lease updated"
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(
            self.request,
            messages.ERROR,
            "An error has occurred while updating the lease"
        )
        return HttpResponseRedirect(self.get_success_url())


class GenerateRentalPDF(ClientOrAgentRequiredMixin,
                        ClientLeaseAccessMixin,
                        View):
    direct = False

    def get_object(self):
        if self.object:
            return self.object
        self.object = get_object_or_404(
            RentalApplication, id=self.kwargs.get('pk')
        )
        return self.object

    def get(self, *args, **kwargs):
        rental_app = self.get_object()
        lease_member = rental_app.lease_member
        filename = f'{slugify(lease_member.get_full_name())}.pdf'

        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = f'attachment; filename={filename}'

        html = render_to_string("leases/rental_app/rental_app_pdf.html", {
            'rental_app': lease_member.rentalapplication
        })
        font_config = FontConfiguration()
        HTML(string=html).write_pdf(response, font_config=font_config)

        return response
