from django.db.models import Q


def filter_listings(queryset, params):

    searching_text = params.get('searching_text')
    address = params.get('address')
    unit = params.get('unit')
    hoods = params.getlist('hoods[]')
    price = params.getlist('price[]')
    price_per_bed = params.getlist('price_per_bed[]')
    beds = params.getlist('beds[]')
    baths = params.getlist('baths[]')
    listing_type = params.get('listing_type')
    listing_id = params.get('listing_id')
    size = params.getlist('size[]')
    pets_allowed = params.get('pets_allowed')
    amenities = params.getlist('amenities[]')
    nofeeonly = params.get('nofeeonly')
    owner_pays = params.get('owner_pays')
    exclusive = params.get('exclusive')
    vacant = params.get('vacant')
    draft_listings = params.get('draft_listings')
    date_available = params.get('date_available')

    if searching_text:
        queryset = queryset.filter(
            Q(description__icontains=searching_text) |
            Q(neighborhood__icontains=searching_text)
        )

    if address:
        queryset = queryset.filter(address__icontains=address)

    if unit:
        queryset = queryset.filter(unit__icontains=unit)

    if hoods:
        queryset = queryset.filter(neighborhood__in=hoods)

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

    if listing_type and listing_type != 'any':
        queryset = queryset.filter(listing_type=listing_type)

    if listing_id:
        queryset = queryset.filter(id__startswith=listing_id)

    if size:
        if size[0]:
            queryset = queryset.filter(size__gte=size[0])
        if size[1]:
            queryset = queryset.filter(size__lte=size[1])

    if pets_allowed and pets_allowed != 'any':
        queryset = queryset.filter(pets=pets_allowed)

    if amenities:
        for amenity in amenities:
            queryset = queryset.filter(detail__amenities__name=amenity)

    if nofeeonly == 'true':
        queryset = queryset.filter(no_fee_listing=True)

    if owner_pays == 'true':
        queryset = queryset.filter(owner_pays=True)

    if exclusive == 'true':
        queryset = queryset.filter(detail__exclusive=True)

    if vacant == 'true':
        queryset = queryset.filter(detail__vacant=True)

    if draft_listings == 'true':
        queryset = queryset.filter(status='draft')

    if date_available:
        # format: '2019 6 1'
        splitted_date = date_available.split(" ")
        queryset = queryset.filter(
            date_available__year=splitted_date[0],
            date_available__month=splitted_date[1],
            date_available__day=splitted_date[2],
        )

    if price_per_bed:
        prices_per_bed = {str(lt.id): lt.price_per_bed for lt in queryset}
        filtered_ids = [lt_id for lt_id, _ in prices_per_bed.items()]

        if price_per_bed[0]:
            filtered_ids = [
                lt_id for lt_id in filtered_ids
                if int(price_per_bed[0]) <= prices_per_bed[lt_id]
            ]
        if price_per_bed[1]:
            filtered_ids = [
                lt_id for lt_id in filtered_ids
                if prices_per_bed[lt_id] <= int(price_per_bed[1])
            ]

        queryset = queryset.filter(id__in=filtered_ids)

    return queryset
