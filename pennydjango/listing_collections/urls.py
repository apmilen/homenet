from django.urls import path

from listing_collections.views import CollectionsList, CollectionDelete


urlpatterns = [
    path('', CollectionsList.as_view(), name='list'),
    path('delete/<uuid:pk>', CollectionDelete.as_view(), name='delete'),
]
