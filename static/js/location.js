let GetUserLOC = new Promise((resolve, reject) => {
    let LAT, LONG;
    if ("geolocation" in navigator) {
        // check if geolocation is supported/enabled on current browser
        navigator.geolocation.getCurrentPosition(
            function success(position) {
                // for when getting location is a success
                LAT = position.coords.latitude;
                LONG = position.coords.longitude;
                
                resolve({
                    latitude: LAT, 
                    longitude: LONG
                });
            },
            function error(error_message) {
                // for when getting location results in an error
                console.error('An error has occurred while retrieving location', error_message);
                reject('An error has occurred while retrieving location');
            }  
        );
    } else {
        // geolocation is not supported
        reject('geolocation is not enabled on this browser');
    }

})

