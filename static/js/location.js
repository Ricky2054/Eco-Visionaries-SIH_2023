function get_lat_long() { 
    let lat, long;
    lat = long = null;

    if ("geolocation" in navigator) {
        // check if geolocation is supported/enabled on current browser
        navigator.geolocation.getCurrentPosition(
            function success(position) {
                // for when getting location is a success
                lat = position.coords.latitude;
                long = position.coords.longitude;
            },
            function error(error_message) {
                // for when getting location results in an error
                console.error('An error has occurred while retrieving location', error_message);
            }  
        );
    } else {
        // geolocation is not supported
        console.log('geolocation is not enabled on this browser')
    }

    return {lat, long};
}