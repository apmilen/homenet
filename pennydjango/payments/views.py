from decimal import Decimal

from django.conf import settings
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.db import transaction, DatabaseError
from django.db.models import Sum

import stripe
from plaid import Client

from penny.mixins import ClientOrAgentRequiredMixin
from payments.models import Transaction
from payments.utils import get_amount_plus_fee
from payments.constants import (
    DEFAULT_PAYMENT_METHOD, CLIENT_TO_APP, FAILED, APPROVED, PAYMENT_METHOD
)
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
            amount_plus_fee = get_amount_plus_fee(amount) / Decimal(100)
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
            request_amount_plus_fee = amt_with_fee * Decimal(100)
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
        fee = amount_plus_fee / Decimal(100) - amount
        amount_to_stripe = int(amount_plus_fee)
        assert request_amount_plus_fee == amount_plus_fee, \
            "The amount plus Stripe fee is inconsistent"
        lease_member = LeaseMember.objects.get(user=request.user)
        token = request.POST['stripeToken']
        
        try:
            with transaction.atomic():

                stripe_transaction = Transaction.objects.create(
                    lease_member=lease_member,
                    transaction_user=request.user,
                    token=token,
                    amount=amount,
                    from_to=CLIENT_TO_APP,
                    payment_method=DEFAULT_PAYMENT_METHOD,
                    fee = fee
                )
                try:
                    stripe_charge = stripe.Charge.create(
                        amount=amount_to_stripe,
                        currency='usd',
                        description='A test charge',
                        source=token,
                        statement_descriptor='Lease payment'
                    )
                except stripe.error.CardError:
                    stripe_transaction.status = FAILED
                    stripe_transaction.save()
                    messages.warning(
                        request, 
                        "There has been a problem with your card"
                    )
                else:
                    stripe_transaction.status = APPROVED
                    stripe_transaction.stripe_charge_id = stripe_charge.id
                    stripe_transaction.save()
                    new_lease_total_peding = self.get_lease_total_pending(lease)
                    if new_lease_total_peding == 0:
                        self.update_lesase_status(lease)              
                    messages.success(request, 'Your payment was successful')       
        except DatabaseError:
            messages.error(
                request, 
                "There has been an error in the database saving the transaction"
            )

        return HttpResponseRedirect(
            reverse('leases:detail-client', args=[client.id])
        )


class PaymentPagePlaid(ClientOrAgentRequiredMixin, TemplateView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            lease = get_object_or_404(Lease, id=kwargs.get('pk'))
            client = LeaseMember.objects.get(user=request.user)
            client_id = client.id
            lease_member = LeaseMember.objects.get(user=request.user)
            amount = Decimal(request.POST.get('amount', 0))
            stripe_plaid_amt = amount * 100
            if amount <= 0:
                messages.error(
                    request, 
                    "Invalid amount to pay"
                )
                return HttpResponseRedirect(
                    reverse('leases:list')
                )

            """if stripe_plaid_amt > lease_total_pending:
                messages.warning(
                    request, 
                    "This amount is more than the pending payment"
                )
                return HttpResponseRedirect(
                    reverse('leases:list')
                )"""

            PLAID_LINK_PUBLIC_TOKEN = request.POST.get('public_token', None)
            ACCOUNT_ID = request.POST.get('account_id', None)
            # Using Plaid's Python bindings (https://github.com/plaid/plaid-python)
            client = Client(
                client_id=settings.PLAID_CLIENT_ID,
                secret=settings.PLAID_SECRET_KEY,
                public_key=settings.PLAID_PUBLIC_KEY,
                environment='sandbox')
            
            exchange_token_response = client.Item.public_token.exchange(
                PLAID_LINK_PUBLIC_TOKEN
            )
            access_token = exchange_token_response['access_token']
            stripe_response = client.Processor.stripeBankAccountTokenCreate(
                access_token, ACCOUNT_ID
            )
            bank_account_token = stripe_response['stripe_bank_account_token']
    
            try:
                with transaction.atomic():
                    
                    plaid_stripe_transaction = Transaction.objects.create(
                        lease_member=lease_member,
                        transaction_user=request.user,
                        amount=amount,
                        from_to=CLIENT_TO_APP,
                        payment_method=PAYMENT_METHOD[3][0]
                    )
                    try:
                        plaid_stripe_charge = stripe.Charge.create(
                            amount=stripe_plaid_amt,
                            currency='usd',
                            source=bank_account_token,
                            description='Test charge from Plaid - Stripe',
                        )
                    except stripe.error.account_invalid:
                        plaid_stripe_transaction.status = FAILED
                        plaid_stripe_transaction.save()
                        messages.warning(
                            request, 
                            "There has been a problem with the transaction"
                        )
                    else:
                        plaid_stripe_transaction.status = APPROVED
                        plaid_stripe_transaction.stripe_charge_id = plaid_stripe_charge.id
                        plaid_stripe_transaction.save()
                        """new_lease_total_peding = self.get_lease_total_pending(lease)
                        if new_lease_total_peding == 0:
                            self.update_lesase_status(lease)"""              
                        messages.success(request, 'Your payment was successful')       
            except DatabaseError:
                messages.error(
                    request, 
                    "There has been an error in the database saving the transaction"
                )
            response = {
                'status': 'complete'
            }
            return JsonResponse(response)