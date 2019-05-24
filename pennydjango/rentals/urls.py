from django.urls import path

from rentals.views import Listings, ListingDetail


urlpatterns = [
    path('', Listings.as_view(), name='listings'),
    path('detail/<pk>', ListingDetail.as_view(), name='listing_detail')
]
