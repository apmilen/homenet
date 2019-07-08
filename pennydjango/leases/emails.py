from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse

from leases.models import LeaseMember


def send_invitation_email(lease_member: LeaseMember):
    name = lease_member.get_full_name()
    lease = lease_member.offer
    member_id = lease_member.id
    listing_desc = lease.listing.full_address
    relative_url = reverse("leases:create-client", args=[member_id])
    url = f'{settings.BASE_URL}{relative_url}'

    subject = render_to_string(
        'email/leases/_invitation.txt',
        context={
            'user': name,
            'listing': listing_desc
        }
    )
    body = render_to_string(
        'email/leases/_invitation_body.txt',
        context={
            'user': name,
            'url': url
        }
    )
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [lease_member.email])
