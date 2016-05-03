var gender_data  = "";

function generate_trendsEth(data_in, department, major, gender){
    document.getElementById('trend_data').innerText = "Regression Analysis for " + department + ", " + major + ", " + gender;
    if(!gender_data) {
        gender_data = (JSON.parse(JSON.stringify(data_in)));
    }

    var data = (JSON.parse(JSON.stringify(gender_data[department][major][gender])))
        // gender_data[department][major][gender];
    var parse = d3.time.format("%Y").parse;
    for (var i = 0; i < data.length;i++){
        data[i].date = parse(data[i].date.toString());
    }

var margin = {top: 80, right: 80, bottom: 80, left: 80},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var ordinal = d3.scale.ordinal()
  .domain(["Actual Enrollment", "Predicted Regression Enrollment"])
  .range([ "rgb(31,119,180)", "rgb(255, 127, 14)"]);
// Scales and axes. Note the inverted domain for the y-scale: bigger is up!
var x = d3.time.scale().range([0, width]),
    y = d3.scale.linear().range([height, 0]),
    xAxis = d3.svg.axis().scale(x).tickSize(-height).tickSubdivide(true),
    yAxis = d3.svg.axis().scale(y).ticks(4).orient("right");

// An area generator, for the light fill.
var area = d3.svg.area()
    .interpolate("monotone")
    .x(function(d) { return x(d.date); })
    .y0(height)
    .y1(function(d) { return y(d.Enrollment); });

// A line generator, for the dark stroke.
var line = d3.svg.line()
    .interpolate("monotone")
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.Enrollment); });

  // Filter to one symbol; the S&P 500.
  var values = data.filter(function(d) {
    return d.symbol == "Real";
  });

  var msft = data.filter(function(d) {
    return d.symbol == "Predicted";
  });


  // Compute the minimum and maximum date, and the maximum price.
  x.domain([msft[0].date, msft[msft.length - 1].date]);
  y.domain([Math.min(d3.min(msft, function(d) { return d.Enrollment; }), d3.min(values, function(d) { return d.Enrollment; })), Math.max(d3.max(msft, function(d) { return d.Enrollment; }),d3.max(values, function(d) { return d.Enrollment; }) )]).nice();

  // Add an SVG element with the desired dimensions and margin.
  var svg = d3.select("#trends").append('svg')
      .attr("id", "trend_id")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  // Add the clip path.
  svg.append("clipPath")
      .attr("id", "clip")
    .append("rect")
      .attr("width", width)
      .attr("height", height);

  // Add the x-axis.
  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  // Add the y-axis.
  svg.append("g")
      .attr("class", "y axis")
      .attr("transform", "translate(" + width + ",0)")
      .call(yAxis);

svg.append("g")
  .attr("class", "legendOrdinal")
  .attr("transform", "translate(20,20)");

var legendOrdinal = d3.legend.color()
  //d3 symbol creates a path-string, for example
  //"M0,-8.059274488676564L9.306048591020996,
  //8.059274488676564 -9.306048591020996,8.059274488676564Z"
  .shape("path", d3.svg.symbol().type("triangle-up").size(150)())
  .shapePadding(10)
  .scale(ordinal);

svg.select(".legendOrdinal")
  .call(legendOrdinal);

  var colors = d3.scale.category10();
  svg.selectAll('.line')
    .data([values, msft])
    .enter()
      .append('path')
        .attr('class', 'line')
        .style('stroke', function(d) {
          return colors(Math.random() * 50);
        })
        .attr('clip-path', 'url(#clip)')
        .attr('d', function(d) {
          return line(d);
        })
        .attr("data-legend",function(d) { return d.symbol});

  /* Add 'curtain' rectangle to hide entire graph */
  var curtain = svg.append('rect')
    .attr('x', -1 * width)
    .attr('y', -1 * height)
    .attr('height', height)
    .attr('width', width)
    .attr('class', 'curtain')
    .attr('transform', 'rotate(180)')
    .style('fill', '#ffffff');

  /* Optionally add a guideline */
  var guideline = svg.append('line')
    .attr('stroke', '#333')
    .attr('stroke-width', 0)
    .attr('class', 'guide')
    .attr('x1', 1)
    .attr('y1', 1)
    .attr('x2', 1)
    .attr('y2', height);

  /* Create a shared transition for anything we're animating */
  var t = svg.transition()
    .delay(750)
    .duration(6000)
    .ease('linear')
    .each('end', function() {
      d3.select('line.guide')
        .transition()
        .style('opacity', 0)
        .remove()
    });

  t.select('rect.curtain')
    .attr('width', 0);
  t.select('line.guide')
    .attr('transform', 'translate(' + width + ', 0)');

  d3.select("#show_guideline").on("change", function(e) {
    guideline.attr('stroke-width', this.checked ? 1 : 0);
    curtain.attr("opacity", this.checked ? 0.75 : 1);
  });

}

function generate_treeEth(data) {

    $('#tree').tree({
        data: data
    });
    $('#tree').bind(
    'tree.click',
        function(event) {
            // The clicked node is 'event.node'
            if(event.node.name == "White" || event.node.name == "Asian" || event.node.name ==  "AfAm" || event.node.name ==  "Hisp" || event.node.name ==  "NativeAmAl" || event.node.name ==  "Foreigner") {
                var gender = event.node.name;
                var major = event.node.parent.name;
                var department = event.node.parent.parent.name;
                d3.select("#trend_id").remove();
                generate_trendsEth(gender_data, department, major, gender);
            }
        }
    );
}