if (jQuery != undefined) {
    var django = {
        'jQuery': jQuery,
    }
}

var GI;

(function($) {

    $(document).ready(function() {

        try {
            var _ = google;
        } catch (ReferenceError) {
            console.log(ReferenceError);
            return;
        }

        var mapDefaults = {
            'mapTypeId': google.maps.MapTypeId.ROADMAP,
            'scrollwheel': false,
            'streetViewControl': true,
            'panControl': false
        };

        var markerDefaults = {
            'draggable': true,
            'animation': google.maps.Animation.DROP
        };

        $('.geoposition-widget').each(function() {
            var $container = $(this),
                $mapContainer = $('<div class="geoposition-map" />'),
                $addressRow = $('<div class="geoposition-address" style="display: none;" />'),
                $searchRow = $('<div class="geoposition-search" />'),
                $searchInput = $('<input>', {'type': 'search', 'placeholder': 'Digite una dirección…', 'class': 'form-control'}),
                $latitudeField = $container.find('input.geoposition:eq(0)'),
                $longitudeField = $container.find('input.geoposition:eq(1)'),
                latitude = parseFloat($latitudeField.val()) || null,
                longitude = parseFloat($longitudeField.val()) || null,
                map,
                mapLatLng,
                mapOptions,
                mapCustomOptions,
                markerOptions,
                markerCustomOptions,
                marker;

            $mapContainer.css('height', $container.attr('data-map-widget-height') + 'px');
            mapCustomOptions = JSON.parse($container.attr('data-map-options'));
            markerCustomOptions = JSON.parse($container.attr('data-marker-options'));

            function doSearch() {
                var gc = new google.maps.Geocoder();
                $searchInput.parent().find('ul.geoposition-results').remove();
                gc.geocode({
                    'address': $searchInput.val()
                }, function(results, status) {
                    if (status == 'OK') {
                        var updatePosition = function(result) {
                            if (result.geometry.bounds) {
                                map.fitBounds(result.geometry.bounds);
                            } else {
                                map.panTo(result.geometry.location);
                                map.setZoom(18);
                            }
                            marker.setPosition(result.geometry.location);
                            google.maps.event.trigger(marker, 'dragend');
                        };
                        if (results.length == 1) {
                            updatePosition(results[0]);
                        } else {
                            var $ul = $('<ul />', {'class': 'geoposition-results'});
                            $.each(results, function(i, result) {
                                var $li = $('<li />');
                                $li.text(result.formatted_address);
                                $li.bind('click', function() {
                                    updatePosition(result);
                                    $li.closest('ul').remove();
                                });
                                $li.appendTo($ul);
                            });
                            $searchInput.after($ul);
                        }
                    }
                });
            }

            function doGeocode() {
                var gc = new google.maps.Geocoder();
                gc.geocode({
                    'latLng': marker.position
                }, function(results, status) {
                    $addressRow.text('');
                    GI = results;
                    if (results && results[0]) {
                        $addressRow.text(results[0].formatted_address);
                    }
                    window.marker = marker;
                });
            }

            var autoSuggestTimer = null;
            $searchInput.bind('keydown', function(e) {
                if (autoSuggestTimer) {
                    clearTimeout(autoSuggestTimer);
                    autoSuggestTimer = null;
                }

                // if enter, search immediately
                if (e.keyCode == 13) {
                    e.preventDefault();
                    doSearch();
                }
                else {
                    // otherwise, search after a while after typing ends
                    autoSuggestTimer = setTimeout(function(){
                        doSearch();
                    }, 1000);
                }
            }).bind('abort', function() {
                $(this).parent().find('ul.geoposition-results').remove();
            });
            $searchInput.appendTo($searchRow);
            $container.append($searchRow, $mapContainer, $addressRow);

            mapLatLng = new google.maps.LatLng(latitude, longitude);

            mapOptions = $.extend({}, mapDefaults, mapCustomOptions);

            if (!(latitude === null && longitude === null && mapOptions['center'])) {
                mapOptions['center'] = mapLatLng;
            }

            if (!mapOptions['zoom']) {
                mapOptions['zoom'] = latitude && longitude ? 15 : 1;
            }

            map = new google.maps.Map($mapContainer.get(0), mapOptions);
            if (typeof window.map == 'undefined'){
                window.map = map;
            }
            if (typeof window.maps == 'undefined'){
                window.maps = new Array();
                window.maps.push(map);
            } else {
                window.maps.push(map);
            }
            markerOptions = $.extend({}, markerDefaults, markerCustomOptions, {
                'map': map
            });
            /**/
            google.maps.event.addListenerOnce(map, 'idle', function() {
               google.maps.event.trigger(map, 'resize');
            });
            /**/

            if (!(latitude === null && longitude === null && markerOptions['position'])) {
                markerOptions['position'] = mapLatLng;
            }

            marker = new google.maps.Marker(markerOptions);
            if (typeof window.marker == 'undefined'){
                window.marker = marker;
            }
            if (typeof window.markers == 'undefined'){
                window.markers = new Array();
                window.markers.push(marker);
            } else {
                window.markers.push(marker);
            }
            google.maps.event.addListener(marker, 'dragend', function() {
                $latitudeField.val(this.position.lat());
                $longitudeField.val(this.position.lng());
                doGeocode();
            });
            if ($latitudeField.val() && $longitudeField.val()) {
                google.maps.event.trigger(marker, 'dragend');
            }

            $latitudeField.add($longitudeField).bind('keyup', function(e) {
                var latitude = parseFloat($latitudeField.val()) || 0;
                var longitude = parseFloat($longitudeField.val()) || 0;
                var center = new google.maps.LatLng(latitude, longitude);
                map.setCenter(center);
                map.setZoom(15);
                marker.setPosition(center);
                doGeocode();
            });
        });
    });
})(django.jQuery);
