from django.urls import path

from listings.views import (
    MainListingCreate, MainListingUpdate, DetailListingUpdate,
    PhotosListingUpdate, ListingDetail, ReviewListing
)


urlpatterns = [
    path('new', MainListingCreate.as_view(), name='create'),
    path('edit/<uuid:pk>', MainListingUpdate.as_view(), name='edit'),
    path('edit/<uuid:pk>/detail', DetailListingUpdate.as_view(), name='detail'),
    path('edit/<uuid:pk>/photos', PhotosListingUpdate.as_view(), name='photos'),
    path('edit/<uuid:pk>/review', ReviewListing.as_view(), name='review'),
    path('<uuid:pk>/detail', ListingDetail.as_view(), name='listing'),
]
