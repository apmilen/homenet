from penny.mixins import MainObjectContextMixin
from listings.models import Listing


class ListingContextMixin(MainObjectContextMixin):
    pk_url_kwarg = 'pk'
    main_model = Listing
    context_name = 'listing'


class WizardMixin(ListingContextMixin):

    def get_object(self, queryset=None):
        self.listing = self.get_main_object()
        queryset = self.get_queryset()
        obj, _ = queryset.get_or_create(listing=self.listing)
        return obj
