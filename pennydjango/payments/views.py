from decimal import Decimal

from django.conf import settings
from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib import messages
from django.db import transaction, DatabaseError

import stripe

from penny.models import User
from penny.mixins import ClientOrAgentRequiredMixin
from payments.models import Transaction
from payments.forms import ManualTransactionForm
from payments.utils import (
    get_amount_plus_fee, get_lease_total_pending, update_lesase_status
)
from payments.constants import (
    PAYMENT_METHOD, DEFAULT_PAYMENT_METHOD, CLIENT_TO_APP, FAILED, APPROVED,
    FROM_TO
)
from leases.models import Lease, LeaseMember


class PaymentPage(ClientOrAgentRequiredMixin, TemplateView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        stripe.api_key = settings.STRIPE_SECRET_KEY

    template_name = 'payments/payments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context 

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            amount = Decimal(request.GET.get('amount', 0))
            amount_plus_fee = get_amount_plus_fee(amount) / Decimal(100)
            return JsonResponse({'total_paid': amount_plus_fee})

    def post(self, request, *args, **kwargs):
        lease = get_object_or_404(Lease, id=kwargs.get('pk'))
        client = LeaseMember.objects.get(user=request.user)
        lease_total_pending = get_lease_total_pending(lease)
       
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
                    new_lease_total_peding = get_lease_total_pending(lease)
                    if new_lease_total_peding == 0:
                        update_lesase_status(lease)              
                    messages.success(request, 'Your payment was successful')       
        except DatabaseError:
            messages.error(
                request, 
                "There has been an error in the database saving the transaction"
            )

        return HttpResponseRedirect(
            reverse('leases:detail-client', args=[client.id])
        )


class ManualTransaction(ClientOrAgentRequiredMixin, CreateView):    
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            lease_member_id = request.GET.get('lease_member_id', False)
            lease_member = get_object_or_404(LeaseMember, id=lease_member_id)
            context = {
                'form' : ManualTransactionForm(
                    initial={'lease_member': lease_member}
                ),
            }
            response = render_to_string(
                'payments/manual_transaction_form.html',
                context,
                request
            )
            return HttpResponse(response)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            error = False
            form = request.POST
            lease_id = request.POST.get('lease', False)
            lease = get_object_or_404(Lease, id=lease_id)
            lease_member_id = request.POST.get('lease_member', False)
            lease_member = get_object_or_404(LeaseMember, id=lease_member_id)
            entered_by_id = request.POST.get('entered_by', False)
            entered_by = get_object_or_404(User, id=entered_by_id)
            from_to = request.POST.get('from_to', False)
            payment_method = request.POST.get('payment_method', False)
            context = {
                'form': ManualTransactionForm(initial=form)
            }
            
            try:
                amount = Decimal(request.POST['amount'])
            except ValueError:
                messages.error(
                    request, 
                    "Please provide a valid amount"
                )
                
                response = render_to_string(
                    'payments/manual_transaction_form.html',
                    context,
                    request
                )
                return HttpResponse(response)
           
            if amount <= 0:
                error = True
                messages.error(
                    request, 
                    'Invalid amount to pay'
                )

            from_to_options = dict(FROM_TO)
            if not from_to in from_to_options:
                error = True
                messages.error(
                    request, 
                    'Invalid payment method'
                )
                
            valid_payment_method = dict(PAYMENT_METHOD)
            if not payment_method in valid_payment_method:
                error = True
                messages.error(
                    request, 
                    'Invalid payment method'
                )
            
            lease_total_pending = get_lease_total_pending(lease)
            if lease_total_pending == 0:
                messages.warning(
                    request, 
                    "The lease has no pending payments"
                )
                return JsonResponse({'complete': True})
            
            if amount > lease_total_pending:
                messages.warning(
                    request, 
                    "This amount is more than the pending payment"
                )
                return JsonResponse({'complete': True})
            
            if not error:
                try:
                    with transaction.atomic():

                        Transaction.objects.create(
                            lease_member=lease_member,
                            entered_by=entered_by,
                            transaction_user=request.user,
                            amount=amount,
                            from_to=from_to,
                            payment_method=payment_method,
                            status=APPROVED
                        )

                        new_lease_total_peding = get_lease_total_pending(lease)
                        if new_lease_total_peding == 0:
                            update_lesase_status(lease)
                        messages.success(
                            request, 
                            'Your transaction was completed'
                        )
                        return JsonResponse({'complete': True})
                except DatabaseError:
                    messages.error(
                        request,
                        "An error has occurred"
                    )             
                       
            response = render_to_string(
                'payments/manual_transaction_form.html',
                context,
                request
            )

            return HttpResponse(response)
            

            
            
        