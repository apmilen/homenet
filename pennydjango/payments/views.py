from django.shortcuts import render
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from django.db.models import Sum

from penny.mixins import ClientOrAgentRequiredMixin

from django.conf import settings

from penny.models import User

from payments.models import Transaction

from leases.models import Lease, LeaseMember

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentPage(ClientOrAgentRequiredMixin, TemplateView):
    template_name = 'payments/payments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = stripe.api_key
        return context

    def post(self, request, *args, **kwargs):
        lease = get_object_or_404(Lease, id=kwargs.get('pk'))
        lease_cost = lease.moveincost_set.aggregate(Sum('value'))
        lease_cost = lease_cost['value__sum']
        cost_for_stripe = int(lease_cost *100)
        token = request.POST['stripeToken']
        aproved = True
        try:
            stripe.Charge.create(
                amount=cost_for_stripe,
                currency='usd',
                description='A test charge',
                source=token,
                statement_descriptor='Custom descriptor'
            )
            client = LeaseMember.objects.get(user=request.user)           
            messages.success(request, 'Your payment was successfull')
            
        except stripe.error.CardError as e:
            aproved = False
            message.info(request, "There has been a problem with your card")

        Transaction.objects.create(
            service = lease,
            made_by = request.user,
            token = token,
            amount = lease_cost,
            aproved = aproved
        )  

        return HttpResponseRedirect(reverse('leases:detail-client', args=[client.id]))
        
