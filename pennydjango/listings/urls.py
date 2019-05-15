from django.urls import path

from listings.views import MainListingCreate


urlpatterns = [
    path(
        'new', MainListingCreate.as_view(), name='listing_create'
    )
]
