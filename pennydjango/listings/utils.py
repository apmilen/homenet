from django.db.models import Q


def filter_listings(queryset, params):

    searching_text = params.get('searching_text')
    price = params.getlist('price[]')
    beds = params.getlist('beds[]')
    baths = params.getlist('baths[]')
    pets_allowed = params.get('pets_allowed')
    amenities = params.getlist('amenities[]')
    nofeeonly = params.get('nofeeonly')
    draft_listings = params.get('draft_listings')

    if searching_text:
        queryset = queryset.filter(
            Q(description__icontains=searching_text) |
            Q(neighborhood__icontains=searching_text)
        )

    if price:
        if price[0]:
            queryset = queryset.filter(price__gte=price[0])
        if price[1]:
            queryset = queryset.filter(price__lte=price[1])

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

    if draft_listings == 'true':
        queryset = queryset.filter(status='draft')

    return queryset
