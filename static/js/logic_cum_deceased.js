// // Read the data
// d3.csv("../data/chartdata.csv").then(function(data) {
//     // console.log(data);
//     // if (data['country'] === "United States of America") {
//     //     console.log(data.cumulative_deceased)
//     // }
//     // // List of groups (here I have one group per column)
//     var allGroup = ['Albania', 'Andorra', 'Argentina', 'Aruba', 'Australia', 'Austria',
//                     'Azerbaijan', 'Bahrain', 'Bangladesh', 'Belarus', 'Belgium',
//                     'Bermuda', 'Bolivia', 'Brazil', 'Bulgaria', 'Cambodia', 'Canada',
//                     'Cayman Islands', 'Chile', 'Colombia', 'Costa Rica', 'Croatia',
//                     'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Dominica',
//                     'Dominican Republic', 'Ecuador', 'El Salvador',
//                     'Equatorial Guinea', 'Estonia', 'Falkland Islands',
//                     'Faroe Islands', 'Finland', 'France', 'Germany', 'Gibraltar',
//                     'Greece', 'Greenland', 'Guatemala', 'Guernsey', 'Guinea',
//                     'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran',
//                     'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Japan', 'Jersey',
//                     'Jordan', 'Kazakhstan', 'Kuwait', 'Laos', 'Latvia', 'Lebanon',
//                     'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malaysia', 'Maldives',
//                     'Malta', 'Marshall Islands', 'Mexico', 'Moldova', 'Monaco',
//                     'Montenegro', 'Montserrat', 'Morocco', 'Netherlands',
//                     'New Zealand', 'Norway', 'Oman', 'Palau', 'Palestine', 'Panama',
//                     'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Romania',
//                     'Russia', 'Saint Helena', 'San Marino', 'Serbia', 'Seychelles',
//                     'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia',
//                     'South Africa', 'South Korea', 'Spain', 'Sweden', 'Switzerland',
//                     'Thailand', 'Tunisia', 'Turkey', 'Ukraine', 'United Arab Emirates',
//                     'United Kingdom', 'United States of America', 'Uruguay',
//                     'Zimbabwe']

//     function filterdata(country_name){
//         var otherdata = [[],[]]
//         data.forEach(function(d) {
//             if (d['country'] === country_name) {
//                 otherdata[0].push(d.date)
//                 otherdata[1].push(d.cum_deceased)
//             }
//         // return otherdata
//         });
//         console.log(otherdata)
//         return otherdata
//     }

//     function dropdown() {
//         //read the data
//         //console.log(data);
//         //get the name id to the dropdown menu
//         allGroup.forEach(function(country) {
//             d3.select("#selectButton")
//             .append("option")
//             .text(country)
//             .property("value");
//         });
//         var tempdata2 = filterdata(allGroup[0]);
//         linechart(tempdata2);
//     };

//     //change event function
//     function optionChanged(country_name){
//         var tempdata = filterdata(country_name);
//         linechart(tempdata);
//     };

//     function linechart(tempdata){
//         console.log(tempdata[0])
//         var trace1 = {
//             x: tempdata[0],
//             y: tempdata[1],
//             mode: 'lines',
//             type: 'scatter'
//         };
//         var data = [trace1];

//         var layout = {
//             xaxis: {
//               title: 'Date'
//             },
//             yaxis: {
//               title: 'Cumulative Deaths'
//             },
//             title:'Cumulative Deaths Over Time'
//           };
        
//         Plotly.newPlot('my_dataviz', data, layout)
//     }

//     dropdown();
// });

var allGroup = ['Global','Albania', 'Andorra', 'Argentina', 'Aruba', 'Australia', 'Austria',
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

function dropdown() {
    allGroup.forEach(function(country) {
        d3.select("#selectButton")
        .append("option")
        .text(country)
        .property("value");
    });
    filterdata(allGroup[0]);
};

function filterdata(country_name){
    d3.csv("../data/chartdata.csv").then(function(data) {
        var otherdata = [[],[]]
        data.forEach(function(d) {
            if (d['country'] === country_name) {
                otherdata[0].push(d.date)
                otherdata[1].push(d.cum_deceased)
            }
        // return otherdata
        });
        console.log(otherdata)
        
        function linechart(otherdata){
            console.log(otherdata)
            var trace1 = {
                x: otherdata[0],
                y: otherdata[1],
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
        linechart(otherdata)
    });
}

//change event function
function optionChanged(country_name){
    filterdata(country_name);
};

dropdown();
