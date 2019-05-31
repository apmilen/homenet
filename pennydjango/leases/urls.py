from django.urls import path, include
from rest_framework import routers

from leases.views import LeaseCreate, LeasesList, LeaseViewSet, LeaseDetail

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'private', LeaseViewSet)

urlpatterns = [
    path('<uuid:pk>/create', LeaseCreate.as_view(), name='create'),
    path('', LeasesList.as_view(), name='list'),
    path('detail/<uuid:pk>', LeaseDetail.as_view(), name='detail'),
    path('', include(router.urls))
]
