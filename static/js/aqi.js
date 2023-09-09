//content for table
let content = `
<thead>
    <tr
        class="text-md font-semibold tracking-wide text-left text-gray-900 bg-gray-100 uppercase border-b border-gray-600 font-noto">
        <th class="px-4 py-3">Date</th>
        <th class="px-4 py-3">
            SO<sub>2</sub><span class="text-sm lowercase">(&mu;g/m<sup>3</sup>)</span>
        </th>
        <th class="px-4 py-3">
            NO<sub>2</sub><span class="text-sm lowercase">(&mu;g/m<sup>3</sup>)</span>
        </th>
        <th class="px-4 py-3">
            PM10<span class="text-sm lowercase">(&mu;g/m<sup>3</sup>)</span>
        </th>
    </tr>
</thead>`;

//func to get user location details using latitude and longitude
let get_user_loc_details = (lat, long) => {
    $.ajax({
        type: "GET",
        url: "/aqi/api/reverse_geocoding/",
        data: {
            latitude: lat,
            longitude: long
        },
        success: function (response) {
            let data = response.data;
            let error = response.error;
            let status = response.status;
            if(data != null && error == null && status == 200){
                $("#city").html(data.city);
                $("#state").html(data.state);
                $("#country").html(data.country);
            }else if(status == 500){
                alert("INTERNAL SERVER ERROR. TRY AGAIN AFTER SOMETIME")
            }else{
                alert("ERROR: "+error+"  STATUS: "+status)
            }
        }
    });
}

//func to send request for getting current AQI data for given latitude and longitude
let get_current_aqi = (lat, long) => {
    $.ajax({
        type: "GET",
        url: "/aqi/api/get_aqi/",
        data: {
            latitude: lat,
            longitude: long
        },
        success: function (response) {
            let data = response.data;
            let error = response.error;
            let status = response.status;
            if(data != null && error == null && status == 200){
                $("#pm2_5").html(data.pm2_5);
                $("#pm10").html(data.pm10);
                $("#co").html(data.co);
                $("#o3").html(data.o3);
                $("#so2").html(data.so2);
                $("#no2").html(data.no2);
                $("#aqi_status").html(data.aqi_status);
                $("#aqi_status").css("color", data.col);
                $("#aqi_dt").html(data.date);
                
                
                $("#pm2_5_bar").css("width", data.pm2_5_percent);
                $("#pm10_bar").css("width", data.pm10_percent);
                $("#co_bar").css("width", data.co_percent);
                $("#o3_bar").css("width", data.o3_percent);
                $("#so2_bar").css("width", data.so2_percent);
                $("#no2_bar").css("width", data.no2_percent);
            }else if(status == 500){
                alert("INTERNAL SERVER ERROR. TRY AGAIN AFTER SOMETIME")
            }else{
                alert("ERROR: "+error+"  STATUS: "+status)
            }
        }
    });
}

//promise to get historic AQI data for given latitude, longitude and duration
let GetHistoricAQI = (lat, long, dur) =>
    new Promise((resolve, reject) => {
        const ChartData = [['Date', 'SO2', 'NO2', 'PM 10'],];
        $.ajax({
            type: "GET",
            url: "/aqi/api/get_aqi/historic/",
            data: {
                latitude: lat,
                longitude: long,
                duration: dur,
            },
            success: function (response) {
                let data = response.data;
                let error = response.error;
                let status = response.status;

                content += `<tbody class="bg-white">`;

                if(data != null && error == null && status == 200){
                    for (let index = 0; index < data.length; index++) {
                        let date = data[index].date;
                        // let aqi_index = data[index].aqi_index;
                        // let pm2_5 = data[index].pm2_5;
                        let pm10 = data[index].pm10;
                        // let co = data[index].co;
                        let so2 = data[index].so2;
                        // let o3 = data[index].o3;
                        let no2 = data[index].no2;
                        
                        ChartData.push([date, so2, no2, pm10])

                        content += `
                        <tr class="text-gray-700">
                            <td class="px-4 py-3 font-semibold text-sm border">${date}</td>
                            <td class="px-4 py-3 text-ms border">${so2}</td>
                            <td class="px-4 py-3 text-ms border">${no2}</td>
                            <td class="px-4 py-3 text-ms border">${pm10}</td>
                        </tr>                        
                        `; 
                    }
                    content += `</tbody>`;
                    document.getElementById("historic_data_table").innerHTML=content;

                    resolve(ChartData);

                }else if(status == 500){
                    reject("COULD NOT LOAD CHART DUE TO INTERNAL SERVER ERROR");
                }else{
                    reject("ERROR: "+error+"  STATUS: "+status);
                }
            }
        });
})



//when user loc is got then fetch current AQI data
GetUserLOC.then((loc)=>{
    //when loc is got

    let LAT = loc["latitude"], LONG = loc["longitude"];

    //calling the func to get loc details
    get_user_loc_details(LAT, LONG);

    //calling func to get current AQI data
    get_current_aqi(LAT, LONG);      

}).catch((errorMessage)=>{
    //when loc is failed

    console.log("ERROR: "+errorMessage);
})


//when user loc is got then fetch historic AQI data
GetUserLOC.then((loc)=>{
    //when loc is got

    let LAT = loc["latitude"], LONG = loc["longitude"];

    //calling GetHistoricAQI for chart
    GetHistoricAQI(LAT, LONG, "7").then((chart_dara)=>{
        google.charts.load('current', {'packages':['corechart']});
        google.charts.setOnLoadCallback(drawChart);

        function drawChart() {
            var data = google.visualization.arrayToDataTable(chart_dara);

            var options = {
            title: `AQI data from ${chart_dara[1][0]} to ${chart_dara[chart_dara.length-1][0]}`,
            // curveType: 'function',
            vAxes: {
                // Adds titles to each axis.
                0: {title: 'micrograms/meter cube'},
                1: {title: 'Date'}
            },
            legend: { position: 'bottom' }
            };

            $("#historic_aqi_data_chat").css("display", "block");
            var chart = new google.visualization.LineChart(document.getElementById('historic_aqi_data_chat'));


            chart.draw(data, options);
        }

    }).catch((errorMessage)=>{
        console.log(errorMessage)
    })

}).catch((errorMessage)=>{
    //when loc is failed

    console.log("ERROR: "+errorMessage);
})




