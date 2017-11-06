function zoomMapToContainCoords(map, startCoords, finishCoords) {
    if (!startCoords || !finishCoords) return;

    var coords = new google.maps.LatLngBounds();
    coords.extend(startCoords);
    coords.extend(finishCoords);
    map.fitBounds(coords);

    // zoom out map to give spacing between borders and coords
    google.maps.event.addListenerOnce(map, 'bounds_changed', function () {
        map.setZoom(map.getZoom() - 1);
    });
}
