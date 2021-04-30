// google.charts.load('current', {'packages':['corechart']});
// google.charts.setOnLoadCallback(drawChart);

// d3.csv("../data/scatterchartdata.csv").then(function(data) {
//     google.charts.load('current', {'packages':['corechart']});
//     var otherdata = [['Cumulative New People Fully Vaccinated','Average New Confirmed Cases per Day']]
//         data.forEach(function(d) {
//             otherdata.push([parseFloat(d.cum_new_ppl_fully_vaxxed), parseFloat(d.avg_new_confirmed)])
//         // return otherdata
//         });
//     console.log(otherdata)
// });

var otherdata = [['Cumulative New People Fully Vaccinated','Average New Confirmed Cases per Day']]
d3.csv("../data/scatterchartdata.csv").then(function(data) {
    // var otherdata = [['Cumulative New People Fully Vaccinated','Average New Confirmed Cases per Day']]
        data.forEach(function(d) {
            otherdata.push([parseFloat(d.cum_new_ppl_fully_vaxxed), parseFloat(d.avg_new_confirmed)])
        // return otherdata
        });
    console.log(otherdata)
    google.charts.load('current', {callback:drawChart,'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChart);
});

google.charts.load('current', {'packages':['corechart']});
function drawChart() {
    console.log(otherdata)
    var diffdata = google.visualization.arrayToDataTable(
        otherdata
    );
    var options = {
        title: 'Global Cumulative New People Vaccinated vs. Global Average New Confirmed Cases per Day',
        hAxis: {title: 'Cumulative New People Vaccinated', minValue: 0, maxValue: 400000000},
        vAxis: {title: 'Average New Confirmed Cases per Day', minValue: 0, maxValue: 300000},
        legend: 'none'
    };
    var chart = new google.visualization.ScatterChart(document.getElementById('chart_div'));
    chart.draw(diffdata, options);
}
    

// function drawChart(inputdata) {
//     d3.csv("../data/scatterchartdata.csv").then(function(data) {
//         google.charts.load('current', {'packages':['corechart']});
//         google.charts.setOnLoadCallback(drawChart(otherdata));
//         var otherdata = [[],[]]
//         data.forEach(function(d) {
//             otherdata[0].push(parseFloat(d.cum_new_ppl_fully_vaxxed))
//             otherdata[1].push(parseFloat(d.avg_new_confirmed))
//         // return otherdata
//         });

//         var data = google.visualization.arrayToDataTable([
//             otherdata
//         ]);

//         var options = {
//             title: 'Cumulative New People Vaccinated vs. Average New Confirmed Cases per Day',
//             hAxis: {title: 'Cumulative New People Vaccinated', minValue: 0, maxValue: 400000000},
//             vAxis: {title: 'Average New Confirmed Cases per Day', minValue: 0, maxValue: 300000},
//             legend: 'none'
//         };

//         var chart = new google.visualization.ScatterChart(document.getElementById('chart_div'));

//         chart.draw(data, options);
//     });
// }