GetUserLOC.then((loc)=>{
    //when loc is got
    const LAT = loc["latitude"], LONG = loc["longitude"];

    //setting up the map
    var map = L.map('map').setView([LAT, LONG], 13);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="/">Eco Visionaries</a>'
    }).addTo(map);

}).catch((errorMessage)=>{
    //when loc is failed

    console.log("ERROR: "+errorMessage);
})