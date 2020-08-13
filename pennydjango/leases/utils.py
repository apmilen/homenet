import os
import datetime
from dateutil.relativedelta import relativedelta

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
    write_data_pdf(new_pdf_name, pdf_content, css)
    write_merged_pdf(str(rental_app.id), new_pdf_name, 'nys-disclosure', -310)
    delete_merged_pdf(new_pdf_name)


def create_fh_disclosure_pdf(rental_app):
    lease = rental_app.lease_member.offer
    listing = lease.listing
    legal_name = default_if_none(rental_app.lease_member.legal_name)
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
        <p style="margin-top:75px;margin-left: 250px;min-width: 200px;"></p>
        <p style="margin-left: 195px;">{datetime.datetime.today().strftime('%B %d, %Y')}</p>
        <span style="display:block;"></span>
        <p style="margin-top:30px;margin-left: 250px;min-width: 200px;">{legal_name}</p>
        <p style="margin-left: 195px;">{signed_date}</p>
        <br/><br/><br/>
        <p style="display:block;margin-top:45px;10px;line-height: 1.6;">{ip}</p>
        <p style="display:block;margin-left: 0px;width: 740px;">{fh_user_agent}</p>
       '''
    new_pdf_name = 'agreements/fh-disclosure_tmp.pdf'
    write_data_pdf(new_pdf_name, pdf_content, css)
    write_merged_pdf(str(rental_app.id), new_pdf_name, 'FH_disclosure', -180)
    delete_merged_pdf(new_pdf_name)


def write_merged_pdf(rental_id, rental_data_pdf, disclosure_pdf, scale):
    #import pdb; pdb.set_trace()
    disclosure_pdf_name = f'agreements/{disclosure_pdf}.pdf'
    disclosure_pdf_path = os.path.join(settings.STATIC_ROOT, disclosure_pdf_name)
    reader = PdfFileReader(open(disclosure_pdf_path,'rb'))
    writer = PdfFileWriter()
    if reader.getNumPages() > 1:
        writer.addPage(reader.getPage(0))
        page_to_merge = reader.getPage(1)
    else:
        page_to_merge = reader.getPage(0)
    sup_reader = PdfFileReader(open(os.path.join(settings.STATIC_ROOT, rental_data_pdf),'rb'))
    sup_page = sup_reader.getPage(0)
    translated_page = PageObject.createBlankPage(None, sup_page.mediaBox.getWidth(), sup_page.mediaBox.getHeight())
    translated_page.mergeScaledTranslatedPage(page_to_merge, 1, 0, 0)
    translated_page.mergeScaledTranslatedPage(sup_page, 1, 0, scale)
    writer.addPage(translated_page)
    new_nys_name = f'agreements/{disclosure_pdf}_{rental_id}.pdf'
    new_nys_diclosure_path = os.path.join(settings.STATIC_ROOT, new_nys_name)

    with open(new_nys_diclosure_path, 'wb') as f:
            writer.write(f)


def delete_merged_pdf(pdf_name):
    pdf_path = os.path.join(settings.STATIC_ROOT, pdf_name)
    if os.path.exists(pdf_path):
        os.remove(pdf_path)


def write_data_pdf(pdf_name, pdf_content, css):
    new_pdf_path = os.path.join(settings.STATIC_ROOT, pdf_name)
    font_config = FontConfiguration()
    pdf_html = HTML(string=pdf_content)
    pdf_html.write_pdf(
        new_pdf_path, stylesheets=[css],
        font_config=font_config)


def write_rental_data_pdf(rental_app):
    lease = rental_app.lease_member.offer
    listing = lease.listing
    lease_expire = lease.move_in_date + relativedelta(months=+lease.length_of_lease)
    address_padding = 0 if len(default_if_none(listing.address)) > 90 else 18
    current_address_padding = 0 if len(default_if_none(rental_app.current_address)) > 90 else 15
    moving_padding = 0 if len(default_if_none(rental_app.reason_moving)) > 90 else 15
    previous_address_padding = 0 if len(default_if_none(rental_app.previous_address)) > 90 else 10
    job_title_padding = 0 if len(default_if_none(rental_app.job_title)) > 90 else 18
    work_address_padding = 0 if len(default_if_none(rental_app.work_address)) > 90 else 3
    annual_income_padding = 0 if len(default_if_none(rental_app.annual_income)) > 54 else 6
    reference_padding = 0 if len(default_if_none(rental_app.personal_reference)) >= 44 else 15
    landlord_data_padding = get_landlord_row_padding(rental_app)
    previous_landlord_data_padding = get_landlord_row_padding(rental_app, True)

    css = CSS(string='''
        @page {
            size: letter; margin-left: 1cm; margin-right: 0cm; margin-top: 1cm;
        },
        @font-face {src: url(https://fonts.googleapis.com/css2?family=Lilita+One&display=swap)}
        body {
            font-family: "Nunito script=latin rev=1"; font-size: 9px;,
            display:inline-block;
        }
        span {
            display:inline-block;
        }
        div {
            border: 3px solid transparent;
            display: inline-block;
        }
    ''',)
    pdf_content = f'''
        <div style="height: 37px;">
            <span style="width: 240px;margin-left: 120px;padding-top:{address_padding}px;">
                {listing.address}
            </span>
            <span style="width: 125px;margin-left: 62px;">{listing.listing_agent}</span>
            <span style="margin-left: 75px;"></span>
        </div>
        <div style="height: 24px;">
            <span style="width: 50px;margin-left: 124px;padding-top:7px;">
                {lease.length_of_lease} months
            </span>
            <span style="margin-left: 95px;">{listing.price}</span>
            <span style="margin-left: 125px;">{lease.move_in_date.strftime('%b %d, %Y')}</span>
            <span style="margin-left: 70px;">{lease_expire.strftime('%b %d, %Y')}</span>
        </div>
        <br><br>
        <div style="height: 20px;">
            <span style="margin-left: 85px;width: 250px;padding-top:7px;">{rental_app.name}</span>
            <span style="margin-left: 45px;width: 70px">
                {default_if_none(rental_app.date_of_birth)}
            </span>
            <span style="margin-left: 130px;">{rental_app.ssn}</span>
        </div>
        <div style="height: 20px;">
            <span style="margin-left: 115px;width: 230px;padding-top:7px;">
                {default_if_none(rental_app.driver_license)}
            </span>
            <span style="margin-left: 25px;">
                {default_if_none(rental_app.driver_license_state)}
            </span>
        </div>
        <div style="height: 20px;">
            <span style="margin-left: 125px;width: 230px;padding-top:7px;">{rental_app.phone}</span>
            <span style="margin-left: 40px;">{default_if_none(rental_app.work_phone)}</span>
        </div>
        <div style="height: 20px;">
            <span style="margin-left: 100px;width: 260px;padding-top:7px;">{rental_app.email}</span>
            <span style="margin-left: 105px;">{default_if_none(rental_app.cell)}</span>
        </div>
        <div style="height: 30px;">
            <span style="margin-left: 135px;width: 235px;padding-top:{current_address_padding}px;">
                {default_if_none(rental_app.current_address)}
            </span>
            <span style="width: 85px;margin-left: 30px;">
                {default_if_none(rental_app.current_city)}
            </span>
            <span style="width: 75px;margin-left: 50px;">
                {default_if_none(rental_app.current_state)}
            </span>
            <span style="margin-left: 28px;">{default_if_none(rental_app.zipcode)}</span>
        </div>
        <div style="height: 30px;">
            <span style="margin-left: 135px;width: 190px;padding-top:{moving_padding}px;">
                {default_if_none(rental_app.reason_moving)}
            </span>
            <span style="margin-left: 80px;">{default_if_none(rental_app.current_monthly_rent)}</span>
            <span style="width: 100px;margin-left: 160px;">
                {default_if_none(rental_app.current_term)}
            </span>
        </div>
        <div style="height: 32px;">
            <span style="margin-left: 135px;width: 230px;padding-top:{previous_address_padding}px;">
                {default_if_none(rental_app.previous_address)}
            </span>
            <span style="width: 100px;margin-left: 33px;">
                {default_if_none(rental_app.previous_city)}
            </span>
            <span style="width: 70px;margin-left: 39px;">
                {default_if_none(rental_app.previous_state)}
            </span>
            <span style="margin-left: 15px;">{default_if_none(rental_app.previous_zipcode)}</span>
        </div>
        <br/><br/><br/><br/><br/><br/>
        <div style="height: 30px;">
            <span style="margin-left: 142px;width: 183px;padding-top:{job_title_padding}px;">
                {default_if_none(rental_app.job_title)}
            </span>
            <span style="margin-left: 60px;width: 230px;">
                {default_if_none(rental_app.current_company)}
            </span>
        </div>
        <div style="height: 22px;">
            <span style="margin-left: 90px;width: 290px;padding-top:{work_address_padding}px;">
                {default_if_none(rental_app.work_address)}
            </span>
            <span style="margin-left: 110px;width: 200px;">
                {default_if_none(rental_app.time_at_current_job)}
            </span>
        </div>
        <div style="height: 14px;">
            <span style="margin-left: 105px;width: 230px;">
                {default_if_none(rental_app.work_supervisor)}
            </span>
            <span style="margin-left: 90px;width: 180px;">
                {default_if_none(rental_app.supervisor_phone)}
            </span>
        </div>
        <div style="height: 25px;">
            <span style="margin-left: 115px;width: 215px;padding-top:{annual_income_padding}px">
                {default_if_none(rental_app.annual_income)}
            </span>
            <span style="margin-left: 135px;width: 250px;">
                {default_if_none(rental_app.aditional_income)}
            </span>
        </div>
        <div style="height: 23px;padding-top:-5px;">
            <span style="margin-left: 225px;width: 430px;">
                {default_if_none(rental_app.other_payments)}
            </span>
        </div>
        <br/><br/><br/><br/>
        <div style="height: 38px;">
            <span style="margin-left: 132px;width: 135px;padding-top:{landlord_data_padding}px;">
                {default_if_none(rental_app.landlord_name)}
            </span>
            <span style="margin-left: 34px;width: 181px;">
                {default_if_none(rental_app.landlord_address)}
            </span>
            <span style="margin-left: 25px;width: 200px;">
                {default_if_none(rental_app.landlord_contact)}
            </span>
        </div>
        <div style="height: 35px;">
            <span style="margin-left: 133px;width: 143px;padding-top:{previous_landlord_data_padding}px;">
                {default_if_none(rental_app.previous_landlord_name)}
            </span>
            <span style="margin-left: 29px;width: 170px;">
                {default_if_none(rental_app.previous_landlord_address)}
            </span>
            <span style="margin-left: 35px;width: 200px;">
                {default_if_none(rental_app.previous_landlord_phone)}
            </span>
        </div>
        <div style="height: 33px;">
            <span style="margin-left: 142px;width: 115px;padding-top:{reference_padding}px;">
                {default_if_none(rental_app.personal_reference)}
            </span>
            <span style="margin-left: 60px;width: 150px;">
                {default_if_none(rental_app.reference_relationship)}
            </span>
            <span style="margin-left: 37px;width: 200px;">
                {default_if_none(rental_app.personal_reference_phone)}
            </span>
        </div>
        <div style="height: 20px;">
            <span style="margin-left: 215px;width: 25px;padding-top:10px">
                {readable_boolean(rental_app.had_bankruptcy)}
            </span>
            <span style="margin-left: 95px;width: 170px;">
                {readable_boolean(rental_app.had_been_evicted)}
            </span>
            <span style="margin-left: 40px;width: 200px;">
                {readable_boolean(rental_app.had_been_convicted)}
            </span>
        </div>
        <br/><br/><br/><br/><br/><br/><br/><br/>
        <div style="margin-left: 110px;padding-top:17px;">
            <span style=";min-width: 100px;">{rental_app.lease_member.legal_name}</span>
            <span style="margin-left: 300px;min-width: 100px;">
                {datetime.datetime.today().strftime('%B %d, %Y')}
            </span>
        </div>
       '''
    new_pdf_name = f'agreements/renta_app_data_{rental_app.id}.pdf'
    write_data_pdf(new_pdf_name, pdf_content, css)
    write_merged_pdf(str(rental_app.id), new_pdf_name, 'blank_application', -127)
    delete_merged_pdf(new_pdf_name)


def get_rental_app_pdf(rental_app_pdf_name):
    rental_app_pdf = open(os.path.join(settings.STATIC_ROOT, rental_app_pdf_name), 'rb').read()
    return rental_app_pdf


def create_full_rental_app_pdf(rental_app):
    write_rental_data_pdf(rental_app)
    create_nys_disclosure_pdf(rental_app)
    create_fh_disclosure_pdf(rental_app)
    rental_app_pdf_name = f'agreements/rental_app_{rental_app.id}.pdf'
    path = os.path.join(settings.STATIC_ROOT, 'agreements/')
    writer = PdfFileWriter()
    for file in os.listdir(path):
        if file.endswith(str(rental_app.id) +".pdf"):
            pdf_path = path + file
            pdf_reader = PdfFileReader(pdf_path,'rb')
            for page in pdf_reader.pages:
                writer.addPage(page)
            os.remove(pdf_path)

    with open(os.path.join(settings.STATIC_ROOT, rental_app_pdf_name), 'wb') as f:
            writer.write(f)
    rental_app_pdf = get_rental_app_pdf(rental_app_pdf_name)
    delete_merged_pdf(rental_app_pdf_name)
    return rental_app_pdf


def readable_boolean(boolean_field):
    if boolean_field:
         return 'Yes'
    return 'No'


def default_if_none(field_value):
    if field_value is None:
        return ''
    return field_value


def get_landlord_row_padding(rental_app, previous=False):
    name = rental_app.previous_landlord_name if previous else rental_app.landlord_name
    address = rental_app.previous_landlord_address if previous else rental_app.landlord_address
    phone = rental_app.previous_landlord_phone if previous else rental_app.landlord_contact
    landlord_data_max = max([len(default_if_none(name)), len(default_if_none(address)), len(default_if_none(phone))])
    if landlord_data_max >= 57 and landlord_data_max <=78:
        landlord_data_padding = 5
    elif  landlord_data_max >=30 and landlord_data_max <= 56:
        landlord_data_padding = 15
    elif  landlord_data_max <= 29:
        landlord_data_padding = 25
    else:
        landlord_data_padding = 0
    return landlord_data_padding
