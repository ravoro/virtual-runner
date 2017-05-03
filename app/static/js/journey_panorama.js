function initPanorama() {
    startCoords = new google.maps.LatLng(startCoords);
    finishCoords = new google.maps.LatLng(finishCoords);
    var currentCoords = google.maps.geometry.spherical.interpolate(startCoords, finishCoords, fractionCompleted);
    var elementId = 'journey-panorama';

    showNearestPanorama(elementId, currentCoords);
}

function showNearestPanorama(elementId, location) {
    var service = new google.maps.StreetViewService;
    var request = {
        location: location,
        preference: 'best',
        radius: 500 // meters
    };
    var radiusLimit = 10000;  // 10km

    function showPanorama(data) {
        new google.maps.StreetViewPanorama(
            document.getElementById(elementId),
            {
                pano: data.location.pano
            }
        );
    }

    /**
     * Callback function to StreetViewService.getPanorama call.
     *
     * Show the panorama when able to find the nearest panorama within the given radius.
     * If panorama not found, increase the radius and try again. Continue until panorama is found or radiusLimit is reached.
     */
    function callback(data, status) {
        if (data == null) {
            request.radius = request.radius + 500;
            if (request.radius <= radiusLimit) {
                service.getPanorama(request, callback);
            }
        } else {
            showPanorama(data);
        }
    }

    service.getPanorama(request, callback)
}
