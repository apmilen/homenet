from django.urls import path, include
from rest_framework import routers

from listings.views import (
    MainListingCreate, MainListingUpdate, DetailListingUpdate,
    PhotosListingUpdate, ListingDetailView, ReviewListing, Listings,
    PublicListingViewSet, PrivateListingViewSet, UploadPrimaryPhoto,
    UploadExtraPhoto, DeleteExtraPhoto
)

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'public', PublicListingViewSet)
router.register(r'private', PrivateListingViewSet)


urlpatterns = [
    path('', Listings.as_view(), name='listings'),
    path('new', MainListingCreate.as_view(), name='create'),
    path('edit/<uuid:pk>', MainListingUpdate.as_view(), name='edit'),
    path('edit/<uuid:pk>/detail', DetailListingUpdate.as_view(), name='detail'),
    path('edit/<uuid:pk>/photos', PhotosListingUpdate.as_view(), name='photos'),
    path('edit/<uuid:pk>/review', ReviewListing.as_view(), name='review'),
    path('<uuid:pk>/detail', ListingDetailView.as_view(), name='listing'),
    path('<uuid:pk>/photo', UploadPrimaryPhoto.as_view(), name='photo'),
    path('<uuid:pk>/photo-extra',
         UploadExtraPhoto.as_view(),
         name='photo-extra'),
    path('<uuid:pk>/delete-extra',
         DeleteExtraPhoto.as_view(),
         name='delete-extra'),
    path('', include(router.urls))
]
