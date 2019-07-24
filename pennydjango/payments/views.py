from decimal import Decimal

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
from payments.constants import DEFAULT_PAYMENT_METHOD, CLIENT_TO_APP
from leases.models import Lease, LeaseMember, MoveInCost
from leases.constants import LEASE_STATUS


class PaymentPage(ClientOrAgentRequiredMixin, TemplateView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stripe.api_key = settings.STRIPE_SECRET_KEY

    template_name = 'payments/payments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def update_lesase_status(self, lease):
        lease.status = LEASE_STATUS[1][0]
        lease.save()

    def get_lease_total_pending(self, lease):
        lease_total_paid = Transaction.objects.filter(
            lease_member__offer=lease
        ).aggregate(Sum('amount'))
        lease_move_in_costs = MoveInCost.objects.total_by_offer(lease.id)
        lease_total_pending = lease_move_in_costs
        if lease_total_paid['amount__sum'] is not None:
            total_sum = lease_total_paid['amount__sum']
            lease_total_pending = lease_move_in_costs - total_sum
        return lease_total_pending  

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            amount = Decimal(request.GET.get('amount', 0))
            amount_plus_fee = get_amount_plus_fee(amount) / 100
            return JsonResponse({'total_paid': amount_plus_fee})

    def post(self, request, *args, **kwargs):
        lease = get_object_or_404(Lease, id=kwargs.get('pk'))
        client = LeaseMember.objects.get(user=request.user)
        lease_total_pending = self.get_lease_total_pending(lease)
       
        if lease_total_pending == 0:
            messages.warning(
                request, 
                "The lease has no pending payments"
            )
            return HttpResponseRedirect(
                reverse('leases:detail-client', args=[client.id])
            )

        try:
            amount = Decimal(request.POST['amount'])
            amt_with_fee = Decimal(request.POST['amount-plus-fee'])
            request_amount_plus_fee = amt_with_fee * 100
        except ValueError:
            messages.error(
                request, 
                "Please provide a valid amount"
            )
            return HttpResponseRedirect(
                reverse('leases:detail-client', args=[client.id])
            )

        if amount <= 0:
            messages.error(
                request, 
                "Invalid amount to pay"
            )
            return HttpResponseRedirect(
                reverse('leases:detail-client', args=[client.id])
            )

        if amount > lease_total_pending:
            messages.warning(
                request, 
                "This amount is more than the pending payment"
            )
            return HttpResponseRedirect(
                reverse('leases:detail-client', args=[client.id])
            )
       
        amount_plus_fee = get_amount_plus_fee(amount)
        amount_to_stripe = int(amount_plus_fee)
        assert request_amount_plus_fee == amount_plus_fee, \
            "The amount plus Stripe fee is inconsistent"
        lease_member = LeaseMember.objects.get(user=request.user)
        token = request.POST['stripeToken']
        
        try:
            with transaction.atomic():

                Transaction.objects.create(
                    lease_member=lease_member,
                    transaction_user=request.user,
                    token=token,
                    amount=amount,
                    from_to=CLIENT_TO_APP,
                    payment_method=DEFAULT_PAYMENT_METHOD
                )
                stripe.Charge.create(
                    amount=amount_to_stripe,
                    currency='usd',
                    description='A test charge',
                    source=token,
                    statement_descriptor='Lease payment'
                )
                new_lease_total_peding = self.get_lease_total_pending(lease)
                if new_lease_total_peding == 0:
                    self.update_lesase_status(lease)              
                messages.success(request, 'Your payment was successful')
        except stripe.error.CardError:
            messages.warning(request, "There has been a problem with your card")
        except DatabaseError:
            messages.error(
                request, 
                "There has been an error in the database saving the transaction"
            )

        return HttpResponseRedirect(
            reverse('leases:detail-client', args=[client.id])
        )
