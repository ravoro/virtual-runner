function initMap() {
    startCoords = new google.maps.LatLng(startCoords);
    finishCoords = new google.maps.LatLng(finishCoords);
    var elementId = 'journey-map';


    // create map
    var map = new google.maps.Map(document.getElementById(elementId), {
        center: startCoords,
        zoom: 3
    });
    // zoom map to contain all coords
    var coords = new google.maps.LatLngBounds();
    coords.extend(startCoords);
    coords.extend(finishCoords);
    map.fitBounds(coords);
    // zoom out map to give spacing between borders and coords
    google.maps.event.addListenerOnce(map, 'bounds_changed', function () {
        map.setZoom(map.getZoom() - 1);
    });


    // create start/finish markers
    var startMarker = new google.maps.Marker({
        icon: "http://maps.google.com/mapfiles/dd-start.png",
        map: map,
        position: startCoords,
        title: "Start point"
    });
    var finishMarker = new google.maps.Marker({
        icon: "http://maps.google.com/mapfiles/dd-end.png",
        map: map,
        position: finishCoords,
        title: "Finish point"
    });


    // determine current marker
    var currentCoords = google.maps.geometry.spherical.interpolate(startCoords, finishCoords, fractionCompleted);
    var currentMarker = fractionCompleted == 0 ? startMarker : new google.maps.Marker({
        map: map,
        position: currentCoords,
        title: "Current point"
    });


    // plot lines
    new google.maps.Polyline({
        map: map,
        path: [startCoords, currentCoords],
        strokeWeight: 5,
        strokeOpacity: 1
    });
    new google.maps.Polyline({
        map: map,
        path: [currentCoords, finishCoords],
        strokeWeight: 5,
        strokeOpacity: 0.3
    });


    // info box
    var infoDetails = $('#journey-distance-details').html();
    new google.maps.InfoWindow({
        content: "<dl>" + infoDetails + "</dl>"
    }).open(map, currentMarker);
}
