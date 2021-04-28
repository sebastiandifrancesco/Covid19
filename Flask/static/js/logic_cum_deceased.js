// // set the dimensions and margins of the graph
// var margin = {top: 60, right: 20, bottom: 60, left: 100},
// width = 1300 - margin.left - margin.right,
// height = 700 - margin.top - margin.bottom;

// // append the svg object to the body of the page
// var svg = d3.select("#my_dataviz")
// .append("svg")
// .attr("width", width + margin.left + margin.right)
// .attr("height", height + margin.top + margin.bottom)
// .append("g")
// .attr("transform",
//       "translate(" + margin.left + "," + margin.top + ")");

// Configure a parseTime function which will return a new Date object from a string
// var parser = d3.timeParse("%Y-%m-%d");
var coviddate;
// d3.json("http://localhost:8000/access_data").then(function(data){
//         coviddate = data
//         console.log(data)})
// Read the data
d3.csv("../data/chartdata.csv").then(function(data) {
    // console.log(data);
    // if (data['country'] === "United States of America") {
    //     console.log(data.cumulative_deceased)
    // }
    // // List of groups (here I have one group per column)
    var allGroup = ['Albania', 'Andorra', 'Argentina', 'Aruba', 'Australia', 'Austria',
                    'Azerbaijan', 'Bahrain', 'Bangladesh', 'Belarus', 'Belgium',
                    'Bermuda', 'Bolivia', 'Brazil', 'Bulgaria', 'Cambodia', 'Canada',
                    'Cayman Islands', 'Chile', 'Colombia', 'Costa Rica', 'Croatia',
                    'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Dominica',
                    'Dominican Republic', 'Ecuador', 'El Salvador',
                    'Equatorial Guinea', 'Estonia', 'Falkland Islands',
                    'Faroe Islands', 'Finland', 'France', 'Germany', 'Gibraltar',
                    'Greece', 'Greenland', 'Guatemala', 'Guernsey', 'Guinea',
                    'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran',
                    'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Japan', 'Jersey',
                    'Jordan', 'Kazakhstan', 'Kuwait', 'Laos', 'Latvia', 'Lebanon',
                    'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malaysia', 'Maldives',
                    'Malta', 'Marshall Islands', 'Mexico', 'Moldova', 'Monaco',
                    'Montenegro', 'Montserrat', 'Morocco', 'Netherlands',
                    'New Zealand', 'Norway', 'Oman', 'Palau', 'Palestine', 'Panama',
                    'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Romania',
                    'Russia', 'Saint Helena', 'San Marino', 'Serbia', 'Seychelles',
                    'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia',
                    'South Africa', 'South Korea', 'Spain', 'Sweden', 'Switzerland',
                    'Thailand', 'Tunisia', 'Turkey', 'Ukraine', 'United Arab Emirates',
                    'United Kingdom', 'United States of America', 'Uruguay',
                    'Zimbabwe']
    // // add the options to the button
    // d3.select("#selectButton")
    // .selectAll('myOptions')
    // .data(allGroup)
    // .enter()
    // .append('option')
    // .text(function (d) { return d; }) // text showed in the menu
    // .attr("value", function (d) { return d; }) // corresponding value returned by the button

    // // A color scale: one color for each group
    // var myColor = d3.scaleOrdinal()
    // .domain(allGroup)
    // .range(d3.schemeSet2);

    // // Format the date and cast the miles value to a number
    // var USdata = [[],[]]
    // data.forEach(function(data) {
    //     // data.date = parser(data.date);
    //     if (data['country'] === "United States of America") {
    //         USdata[0].push(data.date)
    //         USdata[1].push(data.cum_deceased)
    //     }
    // });  

    // console.log(USdata)

    function filterdata(country_name){
        var otherdata = [[],[]]
        data.forEach(function(d) {
            if (d['country'] === country_name) {
                otherdata[0].push(d.date)
                otherdata[1].push(d.cum_deceased)
            }
        // return otherdata
        });
        console.log(otherdata)
        return otherdata
    }

    function dropdown() {
        //read the data
        //console.log(data);
        //get the name id to the dropdown menu
        allGroup.forEach(function(country) {
            d3.select("#selectButton")
            .append("option")
            .text(country)
            .property("value");
        });
        var tempdata2 = filterdata(allGroup[0]);
        linechart(tempdata2);
    };

    //change event function
    function optionChanged(country_name){
        var tempdata = filterdata(country_name);
        linechart(tempdata);
    };

    function linechart(tempdata){
        console.log(tempdata[0])
        var trace1 = {
            x: tempdata[0],
            y: tempdata[1],
            mode: 'lines',
            type: 'scatter'
        };
        var data = [trace1];

        var layout = {
            xaxis: {
              title: 'Date'
            },
            yaxis: {
              title: 'Cumulative Deaths'
            },
            title:'Cumulative Deaths Over Time'
          };
        
        Plotly.newPlot('my_dataviz', data, layout)
    }

    dropdown();
});

//change event function
function optionChanged(country_name){
    var tempdata = filterdata(country_name);
    linechart(tempdata);
};
