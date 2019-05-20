from django.urls import path

from listings.views import (
    MainListingCreate, MainListingUpdate, DetailListingUpdate,
    PhotosListingUpdate
)


urlpatterns = [
    path('new', MainListingCreate.as_view(), name='create'),
    path('edit/<uuid:pk>', MainListingUpdate.as_view(), name='edit'),
    path('<uuid:pk>/detail', DetailListingUpdate.as_view(), name='detail'),
    path('<uuid:pk>/photos', PhotosListingUpdate.as_view(), name='photos'),
]
