// const cities = [
//     {
//         "geometry": {
//             "latitude": 23.6871297,
//             "longitude":  86.9746587
//         },
//         "properties": {
//             "name": "asansol",
//             "pm10": "32.22",
//             "so2": "26.94",
//             "no2": "20.56"
//         }
//     },
//     {
//         "geometry": {
//             "latitude": 22.3654432,
//             "longitude": 88.4325028
//         },
//         "properties": {
//             "name": "baruipur",
//             "pm10": "27.4",
//             "so2": "9.66",
//             "no2": "5.14"
//         }
//     }
// ]

//promise to get all the city in GeoJSON format
let CityList = new Promise((resolve, reject) => {
    $.ajax({
        type: "get",
        url: "/aqi/api/get_city_list/",
        success: function (response) {
            let data = response.data;
            let status = response.status;
            let error = response.error;

            if(data != null && status == 200 && error == null){
                resolve(data);
            }else{
                reject("Error: "+error+" Status: "+status);
            }
        }
    });
})

//func to make popup content for city aqi
let cityAQIPopupContent = (data) => {
    let content = `
        <div class="font-noto popup-box">
            <h4 class="capitalize">City: ${data.properties.name}</h4>
            <div class="aqi_content">
                <p> Condition: <span class="uppercase font-bold">${data.properties.aqi_status}</span></p>
                <div class="flex">
                    <p>SO2: <span class="font-bold">${data.properties.so2}</span></p>
                    <p style="margin: 0 0.35rem;">NO2: <span class="font-bold">${data.properties.no2}</span></p>
                    <p>PM10: <span class="font-bold">${data.properties.pm10}</span></p>
                </div>
            </div>
        </div>
    `;

    return content;
}


// // func to make fly animation
// let flyMap = (lat, long)=>{
//     console.log(lat)
//     console.log(map)
//     map.flyTo([long, lat]);
// }


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
        iconUrl: '/static/images/user_location.png',
        iconSize: [30, 30]
    });
    let markerLOC = L.marker([LAT, LONG], {
        icon: userIcon
    }).bindPopup('<h3 class="font-noto" id="your_location_pin">Your Location</h3>').addTo(map);


    //setting up the map when city list is fetched
    const cityIcon = L.icon({
        iconUrl: '/static/images/location.png',
        iconSize: [25, 25]
    })
    CityList.then((cities) => {
        for (item of cities) {
            L.marker([item.geometry.latitude, item.geometry.longitude], {
                icon: cityIcon
            }).bindPopup(cityAQIPopupContent(item)).addTo(map);
        }        
    }).catch((errorMessage)=>{
        //when data fetching is failed
        console.log("Error: "+errorMessage);
    })


}).catch((errorMessage)=>{
    //when loc is failed

    console.log("ERROR: "+errorMessage);
})


