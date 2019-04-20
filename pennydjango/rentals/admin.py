from django.contrib import admin


from .models import RentProperty
from .forms import CreateRentPropertyForm

from mapwidgets.widgets import GooglePointFieldWidget


class RentPropertyForm(CreateRentPropertyForm):
    class Meta(CreateRentPropertyForm.Meta):
        widgets = {
            'geopoint': GooglePointFieldWidget()
        }


class RentPropertyAdmin(admin.ModelAdmin):
    form = RentPropertyForm

    list_display = ('address', 'contact', 'about',
                    'price_tag', 'bedrooms', 'baths')

    def price_tag(self, obj):
        return "${:,}".format(obj.price)
    price_tag.short_description = "Price per month"

    def save_model(self, request, obj, form, change):
        obj.publisher = request.user
        super().save_model(request, obj, form, change)


admin.site.register(RentProperty, RentPropertyAdmin)
