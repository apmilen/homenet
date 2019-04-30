from django.urls import path

from ui.views.pages import Home
from ui.views.listings import ListingDetail
from ui.views.accounts import Signup, UserProfile

urlpatterns = [
    path(
        'listings/detail/<pk>', ListingDetail.as_view(), name='listing_detail'
    ),
    path('user/<username>/', UserProfile.as_view(), name="userprofile"),
    path('signup', Signup.as_view(), name='signup'),
    path('', Home.as_view()),
]
