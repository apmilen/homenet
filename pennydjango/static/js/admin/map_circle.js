/**
 * Create a map with a marker.
 */
;(function($) {

  // If we don't have a lat/lon in the input fields,
  // this is where the map will be centered initially.
  var initial_lat = 40.724727,
      initial_lon = -73.996145;

  function initMap() {
    var $prevEl = $('.form-row.field-radius');

    if ($prevEl.length === 0) {
      // Can't find where to put the map.
      return;
    };

    $prevEl.after( $('<div class="js-setloc-map setloc-map"></div>') );
    var mapEl = document.getElementsByClassName('js-setloc-map')[0];

    $('.form-row.field-latitude').hide()
    $('.form-row.field-longitude').hide()

    var lat_div = $('.form-row.field-latitude').children().children()[1]
    var lon_div = $('.form-row.field-longitude').children().children()[1]
    var lat = parseFloat(lat_div.innerText);
    var lon = parseFloat(lon_div.innerText);
    var center = {lat: lat || initial_lat, lng: lon || initial_lon}
    var radius = parseInt($('#id_radius').val())


    var map = new google.maps.Map(mapEl, {
      zoom: 12,
      center
    });

    var area = new google.maps.Circle({
      strokeColor: '#FF0000',
      strokeOpacity: 0.8,
      strokeWeight: 2,
      fillColor: '#FF0000',
      fillOpacity: 0.35,
      map,
      center,
      radius
    });

    map.fitBounds(area.getBounds())

  };


  $(document).ready(function(){
    initMap();
  });

})(django.jQuery);