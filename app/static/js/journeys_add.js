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
            calculateDistance();
        });
    }

    function calculateDistance() {
        function NanAsNull(val) {
            return isNaN(val) ? null : val;
        }

        var startLat = NanAsNull(parseFloat(document.getElementById("startLat").value));
        var startLng = NanAsNull(parseFloat(document.getElementById("startLng").value));
        var finishLat = NanAsNull(parseFloat(document.getElementById("finishLat").value));
        var finishLng = NanAsNull(parseFloat(document.getElementById("finishLng").value));

        var totalDistance = null;
        if (startLat && startLng && finishLat && finishLng) {
            var startCoords = new google.maps.LatLng({lat: startLat, lng: startLng});
            var finishCoords = new google.maps.LatLng({lat: finishLat, lng: finishLng});
            totalDistance = google.maps.geometry.spherical.computeDistanceBetween(startCoords, finishCoords);
            totalDistance = totalDistance.toFixed(0);
        }
        document.getElementById("distance-meters").value = totalDistance;
    }
}
