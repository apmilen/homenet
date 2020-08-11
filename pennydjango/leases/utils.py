import os
import datetime

from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.pdf import PageObject

from django.conf import settings
from django.db.models import Q, Sum
from django.utils import timezone


def qs_from_filters(queryset, params):

    address = params.get('address')
    unit = params.get('unit')
    listing_agents = params.getlist('listing_agents[]')
    hoods = params.getlist('hoods[]')
    price = params.getlist('price[]')
    beds = params.getlist('beds[]')
    lease_id = params.get('lease_id')
    lease_status = params.getlist('lease_status[]')

    if address:
        queryset = queryset.filter(listing__address__icontains=address)

    if unit:
        queryset = queryset.filter(listing__unit_number__icontains=unit)

    if listing_agents:
        queryset = queryset.filter(
            listing__listing_agent__email__in=listing_agents)

    if hoods:
        queryset = queryset.filter(listing__neighborhood__in=hoods)

    if price:
        if price[0]:
            queryset = queryset.filter(listing__price__gte=price[0])
        if price[1]:
            queryset = queryset.filter(listing__price__lte=price[1])

    if beds:
        query = Q(
            listing__bedrooms__in=[num for num in beds if '+' not in num]
        )
        plus_nums = [num for num in beds if '+' in num]
        if plus_nums:
            query = query | Q(listing__bedrooms__gte=plus_nums[0][:-1])

        queryset = queryset.filter(query)

    if lease_id:
        queryset = queryset.filter(id__startswith=lease_id)

    if lease_status:
        queryset = queryset.filter(status__in=lease_status)

    return queryset


def get_lease_pending_payment(lease_transactions, lease_total_move_in_cost):
    total_paid_lease = lease_transactions.aggregate(Sum('amount'))
    lease_pending_payment = lease_total_move_in_cost
    if total_paid_lease['amount__sum'] is not None:
        lease_pending_payment = lease_total_move_in_cost - total_paid_lease['amount__sum']
    return lease_pending_payment


def create_nys_disclosure_pdf(rental_app):
    lease = rental_app.lease_member.offer
    listing = lease.listing
    
    signed_date = ''
    if rental_app.lease_member.signed_nys_disclosure:
        signed_date = rental_app.lease_member.signed_nys_disclosure.strftime('%B %d, %Y')

    ip = ''
    if rental_app.lease_member.nys_disclosure_ip_address:
        ip = f'Electronic signature data: <br/>IP: {rental_app.lease_member.nys_disclosure_ip_address}'

    nys_user_agent = ''
    if rental_app.lease_member.nys_disclosure_user_agent:
        nys_user_agent = f'User Agent: {rental_app.lease_member.nys_disclosure_user_agent}'

    css = CSS(string='''
        @page {
            size: letter; margin-left: 1cm; margin-right: 0cm; margin-top: 1cm;
        },
        @font-face {src: url(https://fonts.googleapis.com/css2?family=Lilita+One&display=swap)}
        body {
            font-family: "Nunito script=latin rev=1"; font-size: 12px;,
            display:inline-block;
        }
        span, p {
            display:inline-block;
        }
        .single-line {
            display:block;
            width: 400px;
        }
    ''',)
    pdf_content = f'''
        <p>
            <span style="width: 216px;margin-left: 180px;margin-top:4px;">{listing.listing_agent}</span>
            <span style="margin-left: 175px;font-size: 11px;">Push Forward Realty Cooperative</span>
        </p>
        <p class="single-line" style="margin-top:40%;margin-left: 40px;">
            {rental_app.lease_member.user}
        </p>
        <p class="single-line" style="margin-top:58px;margin-left: 40px;">
            {rental_app.lease_member.legal_name}
        </p>
        <br/><br/>
        <p class="single-line" style="margin-top:27px;margin-left: 40px;">{signed_date}</p>
        <p class="single-line" style="margin-top:-5px;margin-left: 120px;line-height: 1.6;">{ip}</p>
        <p style="display:block;margin-top:-10px;width: 500px;margin-left: 120px;">{nys_user_agent}</p>
    '''
    new_pdf_name = f'agreements/nys-{str(rental_app.id)}-tmp.pdf'
    write_disclosure_data_pdf(new_pdf_name, pdf_content, css)
    write_merged_disclosure_pdf(str(rental_app.id), new_pdf_name, 'nys-disclosure', -310)
    delete_disclosure_pdf(new_pdf_name)


def create_fh_disclosure_pdf(rental_app):
    lease = rental_app.lease_member.offer
    listing = lease.listing
    landlord = '' if rental_app.landlord_name is None else rental_app.landlord_name
    legal_name = '' if rental_app.lease_member.legal_name is None else rental_app.lease_member.legal_name
    signed_date = ''
    if rental_app.lease_member.signed_fair_housing_disclosure:
        signed_date = rental_app.lease_member.signed_fair_housing_disclosure.strftime('%B %d, %Y')
    ip = ''
    if rental_app.lease_member.fair_housing_disclosure_ip_address:
        ip = f'Electronic signature data: <br/>IP: {rental_app.lease_member.fair_housing_disclosure_ip_address}'
    fh_user_agent = ''
    if rental_app.lease_member.fair_housing_disclosure_user_agent:
        fh_user_agent = f'User Agent: {rental_app.lease_member.fair_housing_disclosure_user_agent}'

    css = CSS(string='''
        @page {
            size: letter; margin-left: 1cm; margin-right: 0cm; margin-top: 1cm;
        },
        @font-face {src: url(https://fonts.googleapis.com/css2?family=Lilita+One&display=swap)}
        body {
            font-family: "Nunito script=latin rev=1"; font-size: 13px;,
            display:inline-block;
        }
        span, p {
            display:inline-block;
        }
    ''',)
    pdf_content = f'''
        <p style="width: 240px;margin-left: 220px;">{listing.listing_agent}</p>
        <p style="display:block;margin-top:10px;width: 240px;margin-left: 70px;">Push Forward Realty Cooperative</p>
        <p style="display:block;margin-top:45px;margin-left: 50px;">{rental_app.lease_member.user}</p>
        <p style="margin-top:75px;margin-left: 250px;min-width: 200px;">{landlord}</p>
        <p style="margin-left: 195px;">{datetime.datetime.today().strftime('%B %d, %Y')}</p>
        <span style="display:block;"></span>
        <p style="margin-top:30px;margin-left: 250px;min-width: 200px;">{legal_name}</p>
        <p style="margin-left: 195px;">{signed_date}</p>
        <br/><br/><br/>
        <p style="display:block;margin-top:45px;10px;line-height: 1.6;">{ip}</p>
        <p style="display:block;margin-left: 0px;width: 740px;">{fh_user_agent}</p>
       '''
    new_pdf_name = 'agreements/fh-disclosure_tmp.pdf'
    write_disclosure_data_pdf(new_pdf_name, pdf_content, css)
    write_merged_disclosure_pdf(str(rental_app.id), new_pdf_name, 'FH_disclosure', -180)
    delete_disclosure_pdf(new_pdf_name)


def write_merged_disclosure_pdf(rental_id, rental_data_pdf, disclosure_pdf, scale):
    disclosure_pdf_name = f'agreements/{disclosure_pdf}.pdf'
    disclosure_pdf_path = os.path.join(settings.STATIC_ROOT, disclosure_pdf_name)
    reader = PdfFileReader(open(disclosure_pdf_path,'rb'))
    first_p = reader.getPage(0)
    second_p = reader.getPage(1)

    sup_reader = PdfFileReader(open(os.path.join(settings.STATIC_ROOT, rental_data_pdf),'rb'))
    sup_page = sup_reader.getPage(0)
    translated_page = PageObject.createBlankPage(None, sup_page.mediaBox.getWidth(), sup_page.mediaBox.getHeight())
    translated_page.mergeScaledTranslatedPage(second_p, 1, 0, 0)
    translated_page.mergeScaledTranslatedPage(sup_page, 1, 0, scale)

    writer = PdfFileWriter()
    writer.addPage(first_p)
    writer.addPage(translated_page)
    new_nys_name = f'agreements/{disclosure_pdf}_{rental_id}.pdf'
    new_nys_diclosure_path = os.path.join(settings.STATIC_ROOT, new_nys_name)

    with open(new_nys_diclosure_path, 'wb') as f:
            writer.write(f)


def delete_disclosure_pdf(pdf_name):
    pdf_path = os.path.join(settings.STATIC_ROOT, pdf_name)
    if os.path.exists(pdf_path):
        os.remove(pdf_path)


def write_disclosure_data_pdf(pdf_name, pdf_content, css):
    new_pdf_path = os.path.join(settings.STATIC_ROOT, pdf_name)
    font_config = FontConfiguration()
    pdf_html = HTML(string=pdf_content)
    pdf_html.write_pdf(
        new_pdf_path, stylesheets=[css],
        font_config=font_config)
