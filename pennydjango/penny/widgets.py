from django import forms
from mapwidgets.settings import mw_settings

from mapwidgets.widgets import GooglePointFieldWidget, minify_if_not_debug


class GooglePointFieldWidgetJQuery(GooglePointFieldWidget):

    @property
    def media(self):
        css = {
            "all": [
                minify_if_not_debug("mapwidgets/css/map_widgets{}.css"),
            ]
        }

        js = [
            "js/jquery-3.2.1.min.js",
            "https://maps.googleapis.com/maps/api/js?libraries=places&language={}&key={}".format(
                mw_settings.LANGUAGE, mw_settings.GOOGLE_MAP_API_KEY
            )
        ]

        if not mw_settings.MINIFED:  # pragma: no cover
            js = js + [
                "mapwidgets/js/jquery_class.js",
                "mapwidgets/js/django_mw_base.js",
                "mapwidgets/js/mw_google_point_field.js",
            ]
        else:
            js = js + [
                "mapwidgets/js/mw_google_point_field.min.js"
            ]

        return forms.Media(js=js, css=css)


class TaggitInput(forms.TextInput):

    def get_context(self, name, value, attrs):
        attrs.update({'class': 'tag-this'})
        return super().get_context(name, value, attrs)

    @property
    def media(self):
        css = {
            "all": [
                'css/jquery.taggit.css',
                'css/taggit-theme.css',
            ]
        }

        js = [
            'js/jquery-3.2.1.min.js',
            'https://code.jquery.com/ui/1.12.0/jquery-ui.min.js',
            "js/tag-it.min.js",
            'js/init-tagit.js'
        ]

        return forms.Media(js=js, css=css)
