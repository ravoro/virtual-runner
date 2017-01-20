function initMap() {
    startCoords = new google.maps.LatLng(startCoords);
    finishCoords = new google.maps.LatLng(finishCoords);


    // create map
    var map = new google.maps.Map(document.getElementById('map'), {
        center: startCoords,
        zoom: 3
    });
    var coords = new google.maps.LatLngBounds();
    coords.extend(startCoords);
    coords.extend(finishCoords);
    map.fitBounds(coords);


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
    var fractionOfTotalCompleted = stagesDistance < totalDistance ? stagesDistance / totalDistance : 1;
    var currentCoords = google.maps.geometry.spherical.interpolate(startCoords, finishCoords, fractionOfTotalCompleted);
    var currentMarker = new google.maps.Marker({
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
    new google.maps.InfoWindow({
        content: "<dl>" +
        "<dt><em>Completion:</em></dt><dd>" + (fractionOfTotalCompleted * 100).toFixed(2) + " %</dd>" +
        "<dt><em>Distance:</em></dt><dd>" + metersToKm(stagesDistance) + " / " + metersToKm(totalDistance) + " km</dd>" +
        ((stagesDistance > totalDistance) ? "<dt><em>Note:</em></dt><dd><em>You've run an additional " + metersToKm(stagesDistance - totalDistance) + " km</em></dd>" : "") +
        "</dl>"
    }).open(map, currentMarker);

    function metersToKm(m) {
        return (m / 1000).toFixed(2);
    }
}
