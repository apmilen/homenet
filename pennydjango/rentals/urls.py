from django.urls import path

from rentals.views import ListingDetail


urlpatterns = [
    path(
        'detail/<pk>', ListingDetail.as_view(), name='listing_detail'
    )
]
