from django.urls import path

from ui.views.pages import Home
from ui.views.accounts import Signup
from ui.views.listings import ListingDetail

urlpatterns = [
    path(
        'listings/detail/<pk>', ListingDetail.as_view(), name='listing_detail'
    ),
    path('signup', Signup.as_view(), name='signup'),
    path('', Home.as_view())
]
