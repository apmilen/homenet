from django.conf import settings
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.db import transaction, DatabaseError
from django.db.models import Sum

import stripe

from penny.mixins import ClientOrAgentRequiredMixin
from payments.models import Transaction
from leases.models import Lease, LeaseMember, MoveInCost
from leases.constants import LEASE_STATUS


class PaymentPage(ClientOrAgentRequiredMixin, TemplateView):
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY

    template_name = 'payments/payments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
            
        return context

    def update_lesase_status(self, lease):
        lease_total_paid = Transaction.objects.filter(
            lease_member__offer=lease
        ).aggregate(Sum('amount'))
        total_move_in_costs = MoveInCost.objects.total_by_offer(lease.id)

        if lease_total_paid['amount__sum'] == total_move_in_costs:
            lease.status = LEASE_STATUS[1][0]
            lease.save()

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = {
                'key':settings.STRIPE_PUBLISHABLE_KEY
            }
            return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        lease = get_object_or_404(Lease, id=kwargs.get('pk'))
        lease_member = LeaseMember.objects.get(user=request.user)
        client = LeaseMember.objects.get(user=request.user)
        token = request.POST['stripeToken']
        amount = request.POST['amount']

        try:
            amount_to_stripe = int(amount * 100) 
        except ValueError:
            messages.error(
                request, 
                "The amount to pay must be a postive value"
            )
            return HttpResponseRedirect(reverse('leases:detail-client', args=[client.id]))
    
        try:
            with transaction.atomic(): 
                stripe.Charge.create(
                    amount=amount_to_stripe,
                    currency='usd',
                    description='A test charge',
                    source=token,
                    statement_descriptor='Custom descriptor'
                )

                Transaction.objects.create(
                    lease_member=lease_member,
                    transaction_user=request.user,
                    token=token,
                    amount=amount
                )
                self.update_lesase_status(lease)               
            messages.success(request, 'Your payment was successfull')
        except stripe.error.CardError:
            messages.warning(request, "There has been a problem with your card")
        except DatabaseError:
            messages.error(
                request, 
                "There has been an error in the database saving the transaction"
            )

        return HttpResponseRedirect(reverse('leases:detail-client', args=[client.id]))
