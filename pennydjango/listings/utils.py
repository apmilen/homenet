from django.db.models import Q


def filter_listings(queryset, params):

    searching_text = params.get('searching_text')
    price_min = params.get('price_min')
    price_max = params.get('price_max')
    beds = params.getlist('beds[]')
    baths = params.getlist('baths[]')
    pets_allowed = params.get('pets_allowed')
    amenities = params.getlist('amenities[]')
    nofeeonly = params.get('nofeeonly')

    if searching_text:
        queryset = queryset.filter(
            Q(description__icontains=searching_text) |
            Q(neighborhood__icontains=searching_text)
        )

    if price_min:
        queryset = queryset.filter(price__gte=price_min)

    if price_max:
        queryset = queryset.filter(price__lte=price_max)

    if beds:
        query = Q(bedrooms__in=[num for num in beds if '+' not in num])
        plus_nums = [num for num in beds if '+' in num]
        if plus_nums:
            query = query | Q(bedrooms__gte=plus_nums[0][:-1])

        queryset = queryset.filter(query)

    if baths:
        query = Q(bathrooms__in=[num for num in baths if '+' not in num])
        plus_nums = [num for num in baths if '+' in num]
        if plus_nums:
            query = query | Q(bathrooms__gte=plus_nums[0][:-1])

        queryset = queryset.filter(query)

    if pets_allowed != 'any':
        queryset = queryset.filter(pets=pets_allowed)

    if amenities:
        for amenity in amenities:
            queryset = queryset.filter(detail__amenities__name=amenity)

    if nofeeonly == 'true':
        queryset = queryset.filter(no_fee_listing=True)

    return queryset
