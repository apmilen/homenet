import re

from django.db import models
from django.utils.functional import cached_property

from penny.constants import NEIGHBORHOODS, AGENT_TYPE
from penny.model_utils import BaseModel
from penny.models import User
from penny.utils import image_path, validate_file_size
from listings.constants import (
    LISTING_TYPES, LISTING_STATUS, MOVE_IN_COST, PETS_ALLOWED, AMENITIES
)


class Listing(BaseModel):
    created_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='listings_created'
    )
    listing_type = models.CharField(
        max_length=255,
        verbose_name='Type',
        choices=LISTING_TYPES)
    price = models.PositiveIntegerField()
    move_in_cost = models.CharField(
        max_length=100, choices=MOVE_IN_COST
    )
    owner_pays = models.PositiveSmallIntegerField(
        verbose_name='Owner pays (private)',
        help_text='Private'
    )
    agent_bonus = models.PositiveIntegerField(verbose_name='Agent Bonus Amount')
    no_fee_listing = models.BooleanField(default=False)
    utilities = models.CharField(max_length=255)
    agent_notes = models.TextField(max_length=250)
    description = models.TextField(max_length=500)
    bedrooms = models.DecimalField(max_digits=3, decimal_places=1)
    size = models.PositiveSmallIntegerField(help_text='sq.feet')
    date_available = models.DateField()
    term = models.CharField(max_length=100)
    pets = models.CharField(max_length=100, choices=PETS_ALLOWED)
    address = models.CharField(max_length=255)
    geopoint = models.CharField(max_length=100)
    unit_number = models.CharField(
        max_length=50,
        verbose_name='Unit Number (Only one)'
    )
    neighborhood = models.CharField(max_length=100, choices=NEIGHBORHOODS)
    listing_agent = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Listing Agent (Private)',
        related_name='listings',
        limit_choices_to={
            'user_type': AGENT_TYPE
        }
    )
    sales_agent = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Sales Agent',
        related_name='listings_as_sales',
        limit_choices_to={
            'user_type': AGENT_TYPE
        }
    )
    status = models.CharField(max_length=50, choices=LISTING_STATUS)

    @cached_property
    def coords(self):
        lon, lat = re.search('\((.+?)\)', self.geopoint).group(1).split()
        return lat, lon

    @cached_property
    def latitude(self):
        return self.coords[0]

    @cached_property
    def longitude(self):
        return self.coords[1]


class Amenity(BaseModel):
    name = models.CharField(max_length=50, choices=AMENITIES)


class ListingDetail(BaseModel):
    listing = models.OneToOneField(
        Listing,
        on_delete=models.CASCADE,
        related_name='detail'
    )
    amenities = models.ManyToManyField(Amenity)
    landlord_contact = models.CharField(
        max_length=150,
        verbose_name='Landlord Contact (Private)'
    )
    building_access = models.TextField(
        max_length=255,
        verbose_name='Building Access (Private)'
    )
    vacant = models.BooleanField(
        default=False,
        help_text='Only check if apartment is vacant!'
    )
    hpd = models.BooleanField(
        default=False,
        help_text='Only check if apartment is on HPD unit!'
    )
    accepts_site_apply = models.BooleanField(default=False)
    listing_agreement = models.FileField(
        null=True,
        help_text=('(Manhattan only) Please provide your listing agreement or'
                   'contact with the owner to prove you can post this listing')
    )
    floorplans = models.FileField(null=True)
    exclusive = models.BooleanField(default=False)
    private = models.BooleanField(default=False)
    # office = models.ForeignKey('penny.Office', on_delete=models.SET_NULL)


class ListingPhotos(BaseModel):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='photos'
    )
    primary_photo = models.ImageField(
        upload_to=image_path,
        validators=[validate_file_size],
        null=True
    )


class ListingPhoto(BaseModel):
    listing = models.ForeignKey(ListingPhotos, on_delete=models.CASCADE)
    photo = models.ImageField(
        upload_to=image_path,
        validators=[validate_file_size]
    )
