//func to set aqi data in box after getting from API
let setAQIData = (aqi_index, aqi_status, col, date, pm10, so2, no2, prominent, pm10_percent, so2_percent, no2_percent, city_name=null)=>{
    if(city_name != null){
        $("#city").html(city_name);
    }

    $("#aqi_index").html(aqi_index);
    $("#aqi_index_box").css("background-color", col);
    $("#aqi_status").html(aqi_status);
    $("#aqi_status").css("color", col);
    $("#aqi_dt").html(date);
    $("#pm10").html(pm10);
    $("#so2").html(so2);
    $("#no2").html(no2);

    $("#prominent_pollutant").html(prominent);
    
    $("#pm10_bar").css("width", pm10_percent);
    $("#so2_bar").css("width", so2_percent);
    $("#no2_bar").css("width", no2_percent);
}


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
                setAQIData(data.aqi_index, data.aqi_status, data.col, data.date, data.pollutants.pm10, data.pollutants.so2, data.pollutants.no2, data.pollutants.prominent, data.pollutant_percent.pm10, data.pollutant_percent.so2, data.pollutant_percent.no2);
            }else if(status == 500){
                alert("INTERNAL SERVER ERROR. TRY AGAIN AFTER SOMETIME")
            }else{
                alert("ERROR: "+error+"  STATUS: "+status)
            }
        }
    });
}


//func to load AQI data based on city
let loadAQICityData = (city)=>{
    $.ajax({
        type: "GET",
        url: `/aqi/api/get_aqi/${city}`,
        success: function (response) {
            let data = response.data;
            let error = response.error;
            let status = response.status;
            if(data != null && error == null && status == 200){
                //update the AQI box
                setAQIData(data.aqi_index, data.aqi_status, data.col, data.date, data.pollutants.pm10, data.pollutants.so2, data.pollutants.no2, data.pollutants.prominent, data.pollutant_percent.pm10, data.pollutant_percent.so2, data.pollutant_percent.no2, city_name=city);

                //display the historic data
                if(data.loc.latitude && data.loc.longitude){
                    plotHistoricAQI(data.loc.latitude, data.loc.longitude, "7")
                    // flyMap(data.loc.latitude, data.loc.longitude);
                }
            }else if(status == 500){
                alert("INTERNAL SERVER ERROR. TRY AGAIN AFTER SOMETIME")
            }else{
                alert("ERROR: "+error+"  STATUS: "+status)
            }
            //make the select city enabled and cursor pointer
            select_city = document.getElementById("select_city");
            if(select_city){
                select_city.disabled = false;
                select_city.style.cursor = "pointer"
            }
        }
    });
}
//calling when new city is selected
$("#select_city").on("change", function () {
    loadAQICityData($("#select_city").val());

    //make the select city disabled and cursor not-allowed
    select_city = document.getElementById("select_city");
    if(select_city){
        select_city.disabled = true;
        select_city.style.cursor = "not-allowed"
    }
});


//promise to get historic AQI data for given latitude, longitude and duration
let GetHistoricAQIData = (lat, long, dur) =>{
    return new Promise((resolve, reject) => {
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

                if(document.getElementById("historic_data_table")){
                    document.getElementById("historic_data_table").innerHTML = ""
                }
                let content = `
                <thead>
                    <tr class="text-md font-semibold tracking-wide text-left text-gray-900 bg-gray-100 uppercase border-b border-gray-600 font-noto">
                        <th class="px-4 py-3">Date</th>
                        <th class="px-4 py-3">
                            AQI
                        </th>
                        <th class="px-4 py-3">
                            SO<sub>2</sub><span class="text-sm lowercase" style="text-transform: lowercase;">(&mu;g/m<sup>3</sup>)</span>
                        </th>
                        <th class="px-4 py-3">
                            NO<sub>2</sub><span class="text-sm lowercase" style="text-transform: lowercase;">(&mu;g/m<sup>3</sup>)</span>
                        </th>
                        <th class="px-4 py-3">
                            PM10<span class="text-sm lowercase" style="text-transform: lowercase;">(&mu;g/m<sup>3</sup>)</span>
                        </th>
                    </tr>
                </thead>
                <tbody class="bg-white">`;

                if(data != null && error == null && status == 200){
                    for (let index = 0; index < data.length; index++) {
                        let date = data[index].date;
                        let pm10 = data[index].pollutants.pm10;
                        let so2 = data[index].pollutants.so2;
                        let no2 = data[index].pollutants.no2;
                        let aqi = data[index].aqi_index;
                        
                        ChartData.push([date, so2, no2, pm10])

                        content += `
                        <tr class="text-gray-700">
                            <td class="px-4 py-3 font-semibold text-sm border">${date}</td>
                            <td class="px-4 py-3 text-ms border">${aqi}</td>
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
}

//func to plot the historic AQI data
let plotHistoricAQI = (LAT, LONG, Duration)=>{
    let graphData = GetHistoricAQIData(LAT, LONG, Duration);
    graphData.then((chart_dara)=>{
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
        //when loc is failed
    
        console.log("ERROR: "+errorMessage);
    })
}


//promise to get future AQI data
let GetFutureAQIData = new Promise((resolve, reject) => {
    const FutureChartData = [['Date', 'SO2', 'NO2', 'PM 10'],];
    $.ajax({
        type: "get",
        url: "/aqi/api/get_future_aqi/",
        success: function (response) {
           let data = response.data;
           let error = response.error;
           let status = response.status;

           if(document.getElementById("future_data_table")){
                document.getElementById("future_data_table").innerHTML = ""
            }
            let content = `
            <thead>
                <tr class="text-md font-semibold tracking-wide text-left text-gray-900 bg-gray-100 uppercase border-b border-gray-600 font-noto">
                    <th class="px-4 py-3">Date</th>
                    <th class="px-4 py-3">
                        AQI
                    </th>
                    <th class="px-4 py-3">
                        SO<sub>2</sub><span class="text-sm lowercase" style="text-transform: lowercase;">(&mu;g/m<sup>3</sup>)</span>
                    </th>
                    <th class="px-4 py-3">
                        NO<sub>2</sub><span class="text-sm lowercase" style="text-transform: lowercase;">(&mu;g/m<sup>3</sup>)</span>
                    </th>
                    <th class="px-4 py-3">
                        PM10<span class="text-sm lowercase" style="text-transform: lowercase;">(&mu;g/m<sup>3</sup>)</span>
                    </th>
                </tr>
            </thead>
            <tbody class="bg-white">`;

            if(data != null && error == null && status == 200){
                for (let index = 0; index < data.length; index++) {
                    let date = data[index].date;
                    let pm10 = data[index].pollutants.pm10;
                    let so2 = data[index].pollutants.so2;
                    let no2 = data[index].pollutants.no2;
                    let aqi = data[index].aqi_index;
                    
                    FutureChartData.push([date, so2, no2, pm10])

                    content += `
                    <tr class="text-gray-700">
                        <td class="px-4 py-3 font-semibold text-sm border">${date}</td>
                        <td class="px-4 py-3 text-ms border">${aqi}</td>
                        <td class="px-4 py-3 text-ms border">${so2}</td>
                        <td class="px-4 py-3 text-ms border">${no2}</td>
                        <td class="px-4 py-3 text-ms border">${pm10}</td>
                    </tr>                        
                    `; 
                }
                content += `</tbody>`;
                document.getElementById("future_data_table").innerHTML=content;
                resolve(FutureChartData);

            }else if(status == 500){
                reject("COULD NOT LOAD CHART DUE TO INTERNAL SERVER ERROR");
            }else{
                reject("ERROR: "+error+"  STATUS: "+status);
            }
        }
    });
})
//func to plot the future/predicted AQI data
let plotFutureAQI = ()=>{

    GetFutureAQIData.then((chart_data)=>{
        google.charts.load('current', {'packages':['corechart']});
        google.charts.setOnLoadCallback(drawChart);

        function drawChart() {
            var data = google.visualization.arrayToDataTable(chart_data);

            var options = {
            title: `AQI data from ${chart_data[1][0]} to ${chart_data[chart_data.length-1][0]}`,
            // curveType: 'function',
            vAxes: {
                // Adds titles to each axis.
                0: {title: 'micrograms/meter cube'},
                1: {title: 'Date'}
            },
            legend: { position: 'bottom' }
            };

            $("#future_aqi_data_chat").css("display", "block");
            var futureChart = new google.visualization.LineChart(document.getElementById('future_aqi_data_chat'));


            futureChart.draw(data, options);
        }

    }).catch((errorMessage)=>{
        //when loc is failed
    
        console.log("ERROR: "+errorMessage);
    })
}



//when user loc is got then fetch current AQI data
GetUserLOC.then((loc)=>{
    //when loc is got

    let LAT = loc["latitude"], LONG = loc["longitude"];

    //calling the func to get loc details
    get_user_loc_details(LAT, LONG);

    //calling func to get current AQI data
    get_current_aqi(LAT, LONG);   
    
    //make the select city disabled and cursor not-allowed
    select_city = document.getElementById("select_city");
    if(select_city){
        select_city.disabled = false;
        select_city.style.cursor = "pointer"
    }

}).catch((errorMessage)=>{
    //when loc is failed
    
    //make the select city disabled and cursor not-allowed
    select_city = document.getElementById("select_city");
    if(select_city){
        select_city.disabled = false;
        select_city.style.cursor = "pointer"
    }

    console.log("ERROR: "+errorMessage);
})


//when user loc is got then fetch historic AQI data
GetUserLOC.then((loc)=>{
    //when loc is got

    let LAT = loc["latitude"], LONG = loc["longitude"];

    //display the graph data
    plotHistoricAQI(LAT, LONG, "7");

}).catch((errorMessage)=>{
    //when loc is failed

    console.log("ERROR: "+errorMessage);
})

//when user loc is got then predict the future data also
GetUserLOC.then((loc)=>{
    //when loc is got

    plotFutureAQI();

}).catch((errorMessage)=>{
    //when loc is failed

    console.log("ERROR: "+errorMessage);
})



