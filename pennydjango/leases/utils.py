from django.db.models import Q, Sum


def get_query_params_as_object(params):
    params_obj = {}
    params_obj["address"] = params.get('address')
    params_obj["unit"] = params.get('unit')
    params_obj["listing_agents"] = params.getlist('listing_agents[]')
    params_obj["hoods"] = params.getlist('hoods[]')
    params_obj["price"] = params.getlist('price[]')
    params_obj["beds"] = params.getlist('beds[]')
    params_obj["lease_id"] = params.get('lease_id')
    params_obj["lease_status"] = params.getlist('lease_status[]')
    return params_obj


def qs_from_filters(queryset, params):
    params_obj = get_query_params_as_object(params)
    if params_obj["address"]:
        queryset = queryset.filter(listing__address__icontains=params_obj["address"])

    if params_obj["unit"]:
        queryset = queryset.filter(listing__unit_number__icontains=params_obj["unit"])

    if params_obj["listing_agents"]:
        queryset = queryset.filter(
            listing__listing_agent__email__in=params_obj["listing_agents"]
        )

    if params_obj["hoods"]:
        queryset = queryset.filter(listing__neighborhood__in=params_obj["hoods"])

    if params_obj["price"]:
        if params_obj["price"][0]:
            queryset = queryset.filter(listing__price__gte=params_obj["price"][0])
        if params_obj["price"][1]:
            queryset = queryset.filter(listing__price__lte=params_obj["price"][1])

    if params_obj["beds"]:
        query = Q(
            listing__bedrooms__in=[num for num in params_obj["beds"] if '+' not in num]
        )
        plus_nums = [num for num in params_obj["beds"] if '+' in num]
        if plus_nums:
            query = query | Q(listing__bedrooms__gte=plus_nums[0][:-1])

        queryset = queryset.filter(query)

    if params_obj["lease_id"]:
        queryset = queryset.filter(id__startswith=params_obj["lease_id"])

    if params_obj["lease_status"]:
        queryset = queryset.filter(status__in=params_obj["lease_status"])

    return queryset


def get_lease_pending_payment(lease_transactions, lease_total_move_in_cost):
    total_paid_lease = lease_transactions.aggregate(Sum('amount'))
    lease_pending_payment = lease_total_move_in_cost
    if total_paid_lease['amount__sum'] is not None:
        lease_pending_payment = lease_total_move_in_cost - total_paid_lease['amount__sum']
    return lease_pending_payment
