from django.db.models import Q


def get_query_params_as_object(params):
    params_obj = {}

    params_obj["searching_text"] = params.get('searching_text')
    params_obj["address"] = params.get('address')
    params_obj["unit"] = params.get('unit')
    params_obj["listing_agents"] = params.getlist('listing_agents[]')
    params_obj["hoods"] = params.getlist('hoods[]')
    params_obj["price"] = params.getlist('price[]')
    params_obj["price_per_bed"] = params.getlist('price_per_bed[]')
    params_obj["beds"] = params.getlist('beds[]')
    params_obj["baths"] = params.getlist('baths[]')
    params_obj["listing_type"] = params.get('listing_type')
    params_obj["listing_id"] = params.get('listing_id')
    params_obj["size"] = params.getlist('size[]')
    params_obj["pets_allowed"] = params.get('pets_allowed')
    params_obj["amenities"] = params.getlist('amenities[]')
    params_obj["nofeeonly"] = params.get('nofeeonly')
    params_obj["owner_pays"] = params.get('owner_pays')
    params_obj["exclusive"] = params.get('exclusive')
    params_obj["vacant"] = params.get('vacant')
    params_obj["draft_listings"] = params.get('draft_listings')
    params_obj["date_available"] = params.get('date_available')
    return params_obj


def qs_from_filters(queryset, params):
    params_obj = get_query_params_as_object(params)

    if params_obj["searching_text"]:
        queryset = queryset.filter(
            Q(description__icontains=params_obj["searching_text"]) |
            Q(neighborhood__icontains=params_obj["searching_text"])
        )

    if params_obj["address"]:
        queryset = queryset.filter(address__icontains=params_obj["address"])

    if params_obj["unit"]:
        queryset = queryset.filter(unit_number__icontains=params_obj["unit"])

    if params_obj["listing_agents"]:
        queryset = queryset.filter(listing_agent__username__in=params_obj["listing_agents"])

    if params_obj["hoods"]:
        queryset = queryset.filter(neighborhood__in=params_obj["hoods"])

    if params_obj["price"]:
        if params_obj["price"][0]:
            queryset = queryset.filter(price__gte=params_obj["price"][0])
        if params_obj["price"][1]:
            queryset = queryset.filter(price__lte=params_obj["price"][1])

    if params_obj["beds"]:
        query = Q(bedrooms__in=[num for num in params_obj["beds"] if '+' not in num])
        plus_nums = [num for num in params_obj["beds"] if '+' in num]
        if plus_nums:
            query = query | Q(bedrooms__gte=plus_nums[0][:-1])

        queryset = queryset.filter(query)

    if params_obj["baths"]:
        query = Q(bathrooms__in=[num for num in params_obj["baths"] if '+' not in num])
        plus_nums = [num for num in params_obj["baths"] if '+' in num]
        if plus_nums:
            query = query | Q(bathrooms__gte=plus_nums[0][:-1])

        queryset = queryset.filter(query)

    if params_obj["listing_type"] and params_obj["listing_type"] != 'any':
        queryset = queryset.filter(listing_type=params_obj["listing_type"])

    if params_obj["listing_id"]:
        queryset = queryset.filter(id__startswith=params_obj["listing_id"])

    if params_obj["size"]:
        if params_obj["size"][0]:
            queryset = queryset.filter(size__gte=params_obj["size"][0])
        if params_obj["size"][1]:
            queryset = queryset.filter(size__lte=params_obj["size"][1])

    if params_obj["pets_allowed"] and params_obj["pets_allowed"] != 'any':
        queryset = queryset.filter(pets=params_obj["pets_allowed"])

    if params_obj["amenities"]:
        for amenity in params_obj["amenities"]:
            queryset = queryset.filter(detail__amenities__name=amenity)

    if params_obj["nofeeonly"] == 'true':
        queryset = queryset.filter(no_fee_listing=True)

    if params_obj["owner_pays"] == 'true':
        queryset = queryset.filter(owner_pays=100)

    if params_obj["exclusive"] == 'true':
        queryset = queryset.filter(detail__exclusive=True)

    if params_obj["vacant"] == 'true':
        queryset = queryset.filter(detail__vacant=True)

    if params_obj["draft_listings"] == 'true':
        queryset = queryset.filter(status='draft')

    if params_obj["date_available"]:
        # format: '2019-6-1'
        splitted_date = params_obj["date_available"].split("-")
        queryset = queryset.filter(
            date_available__year=splitted_date[0],
            date_available__month=splitted_date[1],
            date_available__day=splitted_date[2],
        )

    if params_obj["price_per_bed"]:
        prices_per_bed = {str(lt.id): lt.price_per_bed for lt in queryset}
        filtered_ids = [lt_id for lt_id, _ in prices_per_bed.items()]

        if params_obj["price_per_bed"][0]:
            filtered_ids = [
                lt_id for lt_id in filtered_ids
                if int(params_obj["price_per_bed"][0]) <= prices_per_bed[lt_id]
            ]
        if params_obj["price_per_bed"][1]:
            filtered_ids = [
                lt_id for lt_id in filtered_ids
                if prices_per_bed[lt_id] <= int(params_obj["price_per_bed"][1])
            ]

        queryset = queryset.filter(id__in=filtered_ids)

    return queryset
