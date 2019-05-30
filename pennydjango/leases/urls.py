from django.urls import path

from leases.views import LeaseCreate


urlpatterns = [
    path('<uuid:pk>/create', LeaseCreate.as_view(), name='create'),
]
