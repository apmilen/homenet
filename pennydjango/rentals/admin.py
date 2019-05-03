import os
from PIL import Image

from django.db import models
from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe

from penny.widgets import TaggitInput, GooglePointFieldWidgetJQuery
from .models import RentProperty, RentPropertyImage
from .forms import CreateRentPropertyForm


class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        # return super().render(name, value, attrs, renderer)
        output = []
        if value and getattr(value, "url", None):

            size = '200x200'

            # defining the filename and the mini filename
            filehead, filetail = os.path.split(value.path)
            basename, ext = os.path.splitext(filetail)
            mini = f"{basename}_{size}{ext}"
            filename = value.path
            mini_filename = os.path.join(filehead, mini)
            filehead, filetail = os.path.split(value.url)
            mini_url = f"{filehead}/{mini}"

            # make sure thumbnail is a small version of the original image
            if os.path.exists(mini_filename):
                file_mtime = os.path.getmtime(filename)
                mini_mtime = os.path.getmtime(mini_filename)
                if file_mtime > mini_mtime:
                    os.unlink(mini_filename)

            # if the image wasn't already resized, resize it
            if os.path.exists(filename) and not os.path.exists(mini_filename):
                xy = [int(x) for x in size.split('x')]
                image = Image.open(filename)
                image.thumbnail(xy, Image.ANTIALIAS)
                image.save(mini_filename,
                           image.format,
                           quality=100,
                           optimize=1)

            output.append(f'''
                <a href="{value.url}" target="_blank">
                    <img src="{mini_url}" alt="{str(value)}"/>
                </a>
            ''')

        output.append(super(AdminFileWidget, self).render(
            name, value, attrs, renderer
        ))
        return mark_safe(u''.join(output))


class RentPropertyForm(CreateRentPropertyForm):
    class Meta(CreateRentPropertyForm.Meta):
        widgets = {
            'geopoint': GooglePointFieldWidgetJQuery,
            'amenities': TaggitInput
        }


class RentPropertyImageInline(admin.TabularInline):
    model = RentPropertyImage
    extra = 3
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget}
    }


class RentPropertyAdmin(admin.ModelAdmin):
    form = RentPropertyForm
    inlines = [RentPropertyImageInline, ]

    list_display = ('address', 'contact', 'about',
                    'price_tag', 'bedrooms', 'baths')

    def price_tag(self, obj):
        return "${:,}".format(obj.price)
    price_tag.short_description = "Price per month"

    def save_model(self, request, obj, form, change):
        obj.publisher = request.user
        super().save_model(request, obj, form, change)


admin.site.register(RentProperty, RentPropertyAdmin)
admin.site.site_header = 'HomeNet Admin'
