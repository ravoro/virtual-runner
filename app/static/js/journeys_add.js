function initMap() {
    defaultCoords = new google.maps.LatLng(defaultCoords);
    startCoords = startCoords ? new google.maps.LatLng(startCoords) : null;
    finishCoords = finishCoords ? new google.maps.LatLng(finishCoords) : null;


    // create maps
    var startMap = drawMap("map-start", startCoords);
    var finishMap = drawMap("map-finish", finishCoords);

    function drawMap(mapID, centerCoords) {
        return new google.maps.Map(document.getElementById(mapID), {
            zoom: 8,
            center: centerCoords || defaultCoords
        });
    }


    // create markers
    var startMarker = startCoords ? drawMarker(startMap, startCoords) : null;
    var finishMarker = finishCoords ? drawMarker(finishMap, finishCoords) : null;

    function drawMarker(map, coords) {
        return new google.maps.Marker({
            position: coords,
            map: map
        });
    }


    // add map click listeners
    addMapListener(startMap, startMarker, "startLat", "startLng");
    addMapListener(finishMap, finishMarker, "finishLat", "finishLng");

    function addMapListener(map, marker, latID, lngID) {
        map.addListener('click', function (event) {
            var coords = event.latLng;
            if (marker) {
                marker.setMap(null);
            }
            marker = drawMarker(map, coords);
            document.getElementById(latID).value = coords.lat();
            document.getElementById(lngID).value = coords.lng();
        });
    }
}
