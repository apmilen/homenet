if (!mapboxgl.supported()) {
    alert('Your browser does not support Mapbox GL');
} else {
    $(document).ready(function () {

        function translate_to_string(array) {
            return "POINT (" + array[0] + " " + array[1] + ")"
        }

        function filterRegion (item, region) {
            return item.context.map(function (i) {
                return (i.id.split('.').shift() === 'region' && i.text === region);
            }).reduce(function (acc, cur) { return acc || cur; });
        }

        var input = $("#id_geopoint");
        var marker = new mapboxgl.Marker({
            draggable: false,
            color: map_attr_marker_color,
        });
        var map = new mapboxgl.Map({
            container: 'secret-id-map-mapbox-location-field',
            style: map_attr_style,
            center: map_attr_center,
            zoom: map_attr_zoom,
            minZoom: 10,
        });

        if (input.val()) {
            marker.setLngLat(map_attr_center).addTo(map);
            input.val(translate_to_string(map_attr_center));
        }

        var geocoder = new MapboxGeocoder({
            accessToken: mapboxgl.accessToken,
            mapboxgl: mapboxgl,
            countries: 'us',
            language: 'en-US',
            filter: function (item) {
                return filterRegion(item, "New York")
            }
        });

        if (!map_attr_rotate) {
            map.dragRotate.disable();
            map.touchZoomRotate.disableRotation();
        }
        if (map_attr_track_location_button) {
            map.addControl(new mapboxgl.GeolocateControl({
                positionOptions: {
                    enableHighAccuracy: true
                },
                trackUserLocation: true,
            }));
        }
        if (map_attr_geocoder) {
            map.addControl(geocoder, "top-left");
        }
        if (map_attr_fullscreen_button) {
            map.addControl(new mapboxgl.FullscreenControl());
        }
        if (map_attr_navigation_buttons) {
            map.addControl(new mapboxgl.NavigationControl());
        }

        geocoder.on("result", function (e) {
            var result = e.result

            marker.setLngLat(result.geometry.coordinates).addTo(map);
            input.val(translate_to_string(result.geometry.coordinates));
            $("#id_address").val(result.place_name)

            if (result.place_type[0] == 'address') {
                var context = result.context
                var neighborhoods = context.filter(function (elem) {
                    return elem.id.includes("neighborhood")
                })
                if (neighborhoods.length == 1) {
                    var hood_name = neighborhoods[0].text
                    var hood_snake = hood_name.split("/")[0]
                                              .replace(" ", "_")
                                              .replace("'", "")
                                              .replace(".", "")
                                              .toLowerCase()
                    $("#id_neighborhood").val(hood_snake)
                    $("#select2-id_neighborhood-container").html(hood_name)
                }
            }
        });

    });
}