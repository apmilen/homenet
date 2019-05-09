$(document).on("google_point_map_widget:place_changed",
    function (e, place) {
        $('#id_address').val(place['formatted_address'])
    }
);
