import re
from decimal import Decimal


from django import forms
from django.contrib import admin


from .models import RentProperty

from mapwidgets.widgets import GooglePointFieldWidget


class RentPropertyForm(forms.ModelForm):
    class Meta:
        model = RentProperty
        exclude = ('publisher', 'latitude', 'longitude')
        widgets = {
            'address': GooglePointFieldWidget()
        }


class RentPropertyAdmin(admin.ModelAdmin):
    form = RentPropertyForm

    list_display = ('address', 'contact', 'about',
                    'price_tag', 'bedrooms', 'baths')

    def price_tag(self, obj):
        return "${:,}".format(obj.price)
    price_tag.short_description = "Price per month"

    def save_model(self, request, obj, form, change):
        # import pdb; pdb.set_trace()
        lon, lat = re.search('\((.+?)\)', obj.address).group(1).split()
        obj.latitude = Decimal(lat)
        obj.longitude = Decimal(lon)
        # obj.address = f"{lat}, {lon}"
        obj.publisher = request.user
        super().save_model(request, obj, form, change)


admin.site.register(RentProperty, RentPropertyAdmin)
