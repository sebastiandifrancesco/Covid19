// set the dimensions and margins of the graph
var margin = {top: 60, right: 20, bottom: 60, left: 100},
width = 1300 - margin.left - margin.right,
height = 700 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#my_dataviz")
.append("svg")
.attr("width", width + margin.left + margin.right)
.attr("height", height + margin.top + margin.bottom)
.append("g")
.attr("transform",
      "translate(" + margin.left + "," + margin.top + ")");

// Configure a parseTime function which will return a new Date object from a string
var parser = d3.timeParse("%Y/%m");

//Read the data
d3.csv("all_data.csv", function(data) {

// List of groups (here I have one group per column)
var allGroup = ["Brazil", "India",
                "Mexico", 'UK',
                "US"]

// add the options to the button
d3.select("#selectButton")
  .selectAll('myOptions')
   .data(allGroup)
  .enter()
  .append('option')
  .text(function (d) { return d; }) // text showed in the menu
  .attr("value", function (d) { return d; }) // corresponding value returned by the button

// A color scale: one color for each group
var myColor = d3.scaleOrdinal()
  .domain(allGroup)
  .range(d3.schemeSet2);

// Format the date and cast the miles value to a number
data.forEach(function(data) {
  data.month_year = parser(data.month_year);
  data.US = +data.US;
});  

// Add X axis --> it is a date format
var x = d3.scaleTime()
   .range([0, width])
   .domain(d3.extent(data, data => data.month_year));
svg.append("g")
  .attr("transform", "translate(0," + height + ")")
  .call(d3.axisBottom(x))
  .call(g => g.append("text")
  .attr("x", width/2)
  .attr("y", margin.bottom - 20)
  .attr("fill", "currentColor")
  .attr("text-anchor", "end")
  .text("Month"));

// Add Y axis
var y = d3.scaleLinear()
   .range([height, 0])
   .domain([0, d3.max(data, data => data.US)]);
svg.append("g")
  .call(d3.axisLeft(y))
  .call(g => g.append("text")
  .attr("x", -margin.left)
  .attr("y", -20)
  .attr("fill", "currentColor")
  .attr("text-anchor", "start")
  .text("Number of New Covid Cases"));

// Initialize line with group a
var line = svg
  .append('g')
  .append("path")
    .datum(data)
    .attr("d", d3.line()
      .x(function(d) { return x(+d.month_year) })
      .y(function(d) { return y(+d.US) })
    )
    .attr("stroke", function(d){ return myColor("valueA") })
    .style("stroke-width", 4)
    .style("fill", "none")

// A function that update the chart
function update(selectedGroup) {

  // Create new data with the selection?
  var dataFilter = data.map(function(d){return {date: d.month_year, value:d[selectedGroup]} })

  // Give these new data to update line
  line
      .datum(dataFilter)
      .transition()
      .duration(1000)
      .attr("d", d3.line()
        .x(function(d) { return x(+d.date) })
        .y(function(d) { return y(+d.value) })
      )
      .attr("stroke", function(d){ return myColor(selectedGroup) })
}

// When the button is changed, run the updateChart function
d3.select("#selectButton").on("change", function(d) {
    // recover the option that has been chosen
    var selectedOption = d3.select(this).property("value")
    // run the updateChart function with this selected option
    update(selectedOption)
})

})