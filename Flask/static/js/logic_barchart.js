// Creates headers for columns
var otherdata = [['Country','Percentage of Population Fully Vaccinated']]

// Reads the data in and calls the drawChart function on the data
d3.csv("../data/barchartdata.csv").then(function(data) {
    // var otherdata = [['Cumulative New People Fully Vaccinated','Average New Confirmed Cases per Day']]
        data.forEach(function(d) {
            otherdata.push([d.country, parseFloat(d.perc_ppl_fully_vaxxed)])
        // return otherdata
        });
    console.log(otherdata)
    google.charts.load('current', {callback:drawChart,'packages':['corechart', 'bar']});
    google.charts.setOnLoadCallback(drawChart);
});

// Function for drawing the barchart
google.charts.load('current', {'packages':['corechart']});
function drawChart() {
    console.log(otherdata)
    var diffdata = google.visualization.arrayToDataTable(
        otherdata
    );
    var options = {
        title: 'The Ten Countries Closest to Fully Vaccinating Their Population',
        chartArea: {width: '50%'},
        hAxis: {
          title: 'Percentage of Population Fully Vaccinated',
          minValue: 0
        },
        vAxis: {
          title: 'Country'
        }
      };
    
    var chart = new google.visualization.BarChart(document.getElementById('chart_div'));
    chart.draw(diffdata, options);
}