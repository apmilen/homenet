import re

from django.conf import settings
from django.urls import reverse
from django.db import models
from django.utils.functional import cached_property
from django.core.validators import MaxValueValidator

from optimized_image.fields import OptimizedImageField

from penny.constants import NEIGHBORHOODS, AGENT_TYPE, DEFAUL_RENT_IMAGE
from penny.model_utils import BaseModel
from penny.models import User
from penny.utils import image_path
from listings.constants import (
    LISTING_TYPES, LISTING_STATUS, MOVE_IN_COST, PETS_ALLOWED, AMENITIES, DRAFT,
    PARKING_OPTIONS
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
        choices=LISTING_TYPES
    )
    price = models.PositiveIntegerField()
    move_in_cost = models.CharField(
        max_length=100, choices=MOVE_IN_COST
    )
    owner_pays = models.PositiveSmallIntegerField(
        verbose_name='Owner pays (private)',
        help_text='Private'
    )
    agent_bonus = models.PositiveIntegerField(verbose_name='Agent Bonus Amount')
    no_fee_listing = models.BooleanField(
        default=False,
        help_text="Only check if OP is 100%"
    )
    utilities = models.CharField(max_length=255)
    agent_notes = models.TextField(max_length=500, blank=True)
    description = models.TextField(max_length=1024)
    bedrooms = models.DecimalField(max_digits=3, decimal_places=1)
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1)
    size = models.PositiveSmallIntegerField(help_text='sq.feet')
    date_available = models.DateField()
    term = models.CharField(max_length=100)
    pets = models.CharField(max_length=100, choices=PETS_ALLOWED)
    address = models.CharField(max_length=255)
    geopoint = models.CharField(max_length=100)
    nearby_transit = models.TextField(max_length=500, blank=True, null=True)
    unit_number = models.CharField(
        max_length=50,
        verbose_name='Unit Number (Only one)'
    )
    neighborhood = models.CharField(max_length=100, choices=NEIGHBORHOODS)
    parking = models.CharField(
        max_length=64,
        choices=PARKING_OPTIONS,
        null=True,
        blank=True,
    )    
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
    status = models.CharField(
        max_length=50,
        choices=LISTING_STATUS,
        default=DRAFT
    )

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

    @cached_property
    def default_image(self):
        if hasattr(self, 'photos'):
            try:
                url = self.photos.primary_photo.url
            except ValueError:
                pass
            else:
                return url
        return f'{settings.STATIC_URL}{DEFAUL_RENT_IMAGE}'

    @cached_property
    def images(self):
        if hasattr(self, 'photos'):
            images = [
                listing_image.photo.url
                for listing_image in self.photos.listingphoto_set.all()
                if listing_image.photo
            ]
            images.insert(0, self.default_image)
            return images
        return [self.default_image]

    @cached_property
    def amenities(self):
        if hasattr(self, 'detail'):
            return [amenity.get_name_display()
                    for amenity in self.detail.amenities.all()]
        return []

    @cached_property
    def neighborhood_name(self):
        return self.get_neighborhood_display()

    @cached_property
    def full_address(self):
        return f'{self.address} - Unit: {self.unit_number}'

    @cached_property
    def price_per_bed(self):
        return self.bedrooms and round(self.price / self.bedrooms, 2)

    @cached_property
    def edit_link(self):
        return reverse('listing:edit', args=[str(self.id)])

    @cached_property
    def detail_link(self):
        return reverse('listing:detail', args=[str(self.id)])

    @cached_property
    def listing_link(self):
        return reverse('listing:listing', args=[str(self.id)])

    @cached_property
    def offer_link(self):
        return reverse('leases:create', args=[str(self.id)])

    def photos_link(self):
        return reverse("listing:photos", args=[self.id])

    def change_status_link(self):
        return reverse("listing:change-status", args=[self.id])

    def __json__(self, *attrs):
        return {
            **self.attrs(
                'id',
                'default_image',
                'images',
                'price',
                'address',
                'full_address',
                'description',
                'bedrooms',
                'bathrooms',
                'pets',
                'amenities',
                'neighborhood',
                'no_fee_listing',
                'detail_link',
                'edit_link',
                'price_per_bed',
                'short_id',
                'date_available',
                'utilities',
                'move_in_cost',
                'size',
                'owner_pays',
                'agent_notes',
                'agent_bonus',
                'term',
                'created',
                'modified',
                'status',
                'nearby_transit',
                'parking',
            ),
            'str': str(self),
            'detail': self.detail.__json__(),
            'listing_agent': self.listing_agent.__json__(),
            **(self.attrs(*attrs) if attrs else {}),
        }


class Amenity(BaseModel):
    name = models.CharField(max_length=50, choices=AMENITIES)

    def __str__(self):
        return self.get_name_display()


class ListingDetail(BaseModel):
    listing = models.OneToOneField(
        Listing,
        on_delete=models.CASCADE,
        related_name='detail'
    )
    amenities = models.ManyToManyField(Amenity)
    landlord_contact = models.CharField(
        blank=True,
        max_length=150,
        verbose_name='Landlord Contact (Private)'
    )
    building_access = models.TextField(
        blank=True,
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
    floorplans = models.FileField(null=True)
    exclusive = models.BooleanField(default=False)
    private = models.BooleanField(default=False)
    # office = models.ForeignKey('penny.Office', on_delete=models.SET_NULL)

    def __json__(self, *attrs):
        return {
            **self.attrs(
                'id',
                'vacant',
                'landlord_contact'
            ),
            'str': str(self),
            **(self.attrs(*attrs) if attrs else {}),
        }


class ListingPhotos(BaseModel):
    listing = models.OneToOneField(
        Listing,
        on_delete=models.CASCADE,
        related_name='photos'
    )
    primary_photo = OptimizedImageField(
        upload_to=image_path,
        null=True,
        blank=True
    )


class ListingPhoto(BaseModel):
    listing = models.ForeignKey(ListingPhotos, on_delete=models.CASCADE)
    photo = OptimizedImageField(
        upload_to=image_path,
        blank=True
    )
