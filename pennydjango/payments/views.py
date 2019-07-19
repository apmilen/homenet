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
from payments.utils import get_amount_plus_fee
from leases.models import Lease, LeaseMember, MoveInCost
from leases.constants import LEASE_STATUS


class PaymentPage(ClientOrAgentRequiredMixin, TemplateView):
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY

    template_name = 'payments/payments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def update_lesase_status(self, lease):
        lease.status = LEASE_STATUS[1][0]
        lease.save()
    
    def lease_pending_payment(self, lease):
        pending_payment = False
        lease_total_paid = total_paid_by_lease = Transaction.objects.filter(
            lease_member__offer=lease
        ).aggregate(Sum('amount'))
        lease_move_in_costs = MoveInCost.objects.total_by_offer(lease.id)

        if lease_move_in_costs > lease_total_paid['amount__sum']:
            pending_payment = True

        return pending_payment

    def post(self, request, *args, **kwargs):
        lease = get_object_or_404(Lease, id=kwargs.get('pk'))
        client = LeaseMember.objects.get(user=request.user)

        if not self.lease_pending_payment(lease):
            messages.warning(
                request, 
                "The lease has not pending payment"
            )
            return HttpResponseRedirect(reverse('leases:detail-client', args=[client.id]))

        try:
            amount = float(request.POST['amount'])
            request_amount_plus_fee = float(request.POST['amount-plus-fee'])
        except ValueError:
            messages.error(
                request, 
                "Please provide a valid amount"
            )
            return HttpResponseRedirect(reverse('leases:detail-client', args=[client.id]))

        if amount <= 0:
            messages.error(
                request, 
                "Invalid amount to pay"
            )
            return HttpResponseRedirect(reverse('leases:detail-client', args=[client.id]))
       
        amount_plus_fee = get_amount_plus_fee(amount)
        amount_to_stripe = int(amount_plus_fee * 100)
        assert request_amount_plus_fee == amount_plus_fee, "The amount plus Stripe fee is inconsistent"
        lease_member = LeaseMember.objects.get(user=request.user)
        token = request.POST['stripeToken']

        try:
            with transaction.atomic(): 
                stripe.Charge.create(
                    amount=amount_to_stripe,
                    currency='usd',
                    description='A test charge',
                    source=token,
                    statement_descriptor='Lease payment'
                )

                Transaction.objects.create(
                    lease_member=lease_member,
                    transaction_user=request.user,
                    token=token,
                    amount=amount
                )
               
                if not self.lease_pending_payment(lease):
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
