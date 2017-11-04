function initMap() {
    defaultCoords = new google.maps.LatLng(defaultCoords);
    startCoords = startCoords ? new google.maps.LatLng(startCoords) : null;
    finishCoords = finishCoords ? new google.maps.LatLng(finishCoords) : null;


    // create map
    var mapID = "map-start-finish";
    var map = new google.maps.Map(document.getElementById(mapID), {
        zoom: 8,
        center: startCoords || defaultCoords
    });


    // create markers
    var startMarker = startCoords ? drawStartMarker(startCoords) : null;
    var finishMarker = finishCoords ? drawFinishMarker(finishCoords) : null;

    function drawMarker(map, coords, icon) {
        return new google.maps.Marker({
            position: coords,
            map: map,
            icon: icon
        });
    }

    function drawStartMarker(coords) {
        return drawMarker(map, coords, 'http://maps.google.com/mapfiles/dd-start.png');
    }

    function drawFinishMarker(coords) {
        return drawMarker(map, coords, 'http://maps.google.com/mapfiles/dd-end.png');
    }


    // add marker button click listeners
    var startBtn = document.getElementById('start-marker-btn');
    var finishBtn = document.getElementById('finish-marker-btn');
    startBtn.onclick = function () {
        startBtn.classList.add('active');
        finishBtn.classList.remove('active');
    };
    finishBtn.onclick = function () {
        finishBtn.classList.add('active');
        startBtn.classList.remove('active');
    };
    startBtn.click();


    // add map click listener
    map.addListener('click', function (event) {
        var coords = event.latLng;
        var isFinishBtnActive = finishBtn.classList.contains('active');
        var latID = isFinishBtnActive ? "finishLat" : "startLat";
        var lngID = isFinishBtnActive ? "finishLng" : "startLng";

        if (isFinishBtnActive) {
            if (finishMarker) {
                finishMarker.setMap(null);
            }
            finishMarker = drawFinishMarker(coords);
        } else {
            if (startMarker) {
                startMarker.setMap(null);
            }
            startMarker = drawStartMarker(coords);
        }

        document.getElementById(latID).value = coords.lat();
        document.getElementById(lngID).value = coords.lng();
        calculateDistance();
    });


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
