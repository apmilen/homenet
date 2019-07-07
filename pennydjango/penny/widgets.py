from django.conf import settings
from django import forms

from mapbox_location_field.widgets import MapInput


def parse_point(point):
    if isinstance(point, str):
        if point.startswith("POINT ("):
            return tuple(map(float, point[len("POINT ("):-1].split(" ")))

    return point


class MapGeopoint(MapInput):

    def get_config_settings(self):
        """renders javascript configuration variables definitions"""
        default_map_attrs = {
            "style": "mapbox://styles/mapbox/outdoors-v11",
            "zoom": 16 if self.center_point else 11,
            "center": [-73.934196, 40.667398],
            "marker_color": "blue",
            "rotate": True,
            "geocoder": True,
            "fullscreen_button": True,
            "navigation_buttons": True,
            "track_location_button": False,
        }

        if self.center_point:
            default_map_attrs["center"] = parse_point(self.center_point)

        if self.map_attrs is not None:
            default_map_attrs.update(self.map_attrs)
        js = f"""
<script>
    mapboxgl.accessToken = '{settings.MAPBOX_KEY}';
    {self.map_attrs_to_javascript(default_map_attrs)}
</script>
"""
        return js

    @property
    def media(self):
        js = (
            "js/jquery-3.2.1.min.js",
            "js/mapbox-gl.js",
            "js/mapbox-gl-geocoder.min.js",
            # "mapbox_location_field/js/map_input.js",
            "js/map_input.js",
        )
        css = {
            "all": (
                "mapbox_location_field/css/map_input.css",
                "css/mapbox-gl.css",
                "css/mapbox-gl-geocoder.css",
            )
        }

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
