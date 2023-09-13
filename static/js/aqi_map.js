const cities = [
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [72.82952788802635, 18.920675417289807]
        },
        "properties": {
            "name": "asansol",
            "pm10": "32.22",
            "so2": "26.94",
            "no2": "20.56"
        }
    },
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [72.82815459698692, 18.94324557965778]
        },
        "properties": {
            "name": "uluberia",
            "pm10": "29.26",
            "so2": "10.01",
            "no2": "3.13"
        }
    }
]

// //promise to get all the city in GeoJSON format
let CityList = new Promise((resolve, reject) => {
    // $.ajax({
    //     type: "get",
    //     url: "/aqi/api/get_city_list/",
    //     success: function (response) {
    //         let data = response.data;
    //         let status = response.status;
    //         let error = response.error;

    //         if(data != null && status == 200 && error == null){
    //             resolve(data);
    //         }else{
    //             reject("Error: "+error+" Status: "+status);
    //         }
    //     }
    // });
    resolve(cities);
})

//func to make popup content for city aqi
let cityAQIPopupContent = (city) => {
    let content = `
        <div class="font-noto popup-box">
            <h4>City: ${city.properties.name}</h4>
            <div class="aqi_content">
                <p> Condition: <span class="uppercase font-bold">${city.properties.aqi_status}</span></p>
                <div class="flex">
                    <p>SO2: <span class="font-bold">${city.properties.so2}</span></p>
                    <p style="margin: 0 0.35rem;">NO2: <span class="font-bold">${city.properties.no2}</span></p>
                    <p>PM10: <span class="font-bold">${city.properties.pm10}</span></p>
                </div>
            </div>
        </div>
    `;

    return content;
}

//setting up the map when user loc is ready
GetUserLOC.then((loc)=>{
    //when loc is got
    let LAT = loc["latitude"], LONG = loc["longitude"];

    //setting up the map
    var map = L.map('map').setView([LAT, LONG], 8);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="/">Eco Visionaries</a>'
    }).addTo(map);

    //locating user loc on map
    const userIcon = L.icon({
        iconUrl: '/static/images/location.png',
        iconSize: [30, 30]
    });
    let markerLOC = L.marker([LAT, LONG], {
        icon: userIcon
    }).bindPopup('<h3 class="font-noto p-3.5">Your Location</h3>').addTo(map);


    //setting up the map when city list is fetched
    CityList.then((cities)=>{
        //locating each city for AQI
        const cityIcon = L.icon({
            iconUrl: '/static/images/pin.png',
            iconSize: [25, 25]
        })
        // console.log(cities)
        const cityLayer = L.geoJSON(cities, {
            onEachFeature: (feature, layer)=>{
                layer.bindPopup(cityAQIPopupContent(feature)); 
            },

            pointToLayer: (feature, latlng)=>{
                return L.marker(latlng, {icon: cityIcon});
            }
        }).addTo(map);
    }).catch((errorMessage)=>{
        //when city data fetching is failed
    
        console.log("ERROR: "+errorMessage);
    })


}).catch((errorMessage)=>{
    //when loc is failed

    console.log("ERROR: "+errorMessage);
})



