from django.urls import path

from listing_collections.views import (
    CollectionsList, CollectionDelete, CollectionDetail
)


urlpatterns = [
    path('', CollectionsList.as_view(), name='list'),
    path('delete/<uuid:pk>', CollectionDelete.as_view(), name='delete'),
    path('<slug:slug>', CollectionDetail.as_view(), name='detail'),
]
