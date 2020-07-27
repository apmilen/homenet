from django.db.models import Q, Sum


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
