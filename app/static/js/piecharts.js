var department_data = "";
var major_data = "";
var department_clicked = "Engineering";
var year = "fa04";
var major = "Computer Science";
var department_pie_viz = null;
var major_pie_viz = null;
var ethinicity_data = "";
var ethinicity_line_viz = null;
var gender_data = "";

function department_pie(data) {
    department_data = data;
    if (department_pie_viz != null) {
        department_pie_viz.destroy();
        department_pie_viz = null;
    }
    department_pie_viz = new d3pie("pie", {
        "size": {
            "canvasHeight": 375,
            "canvasWidth": 600,
            "pieOuterRadius": "90%"
        },
        data: {
            "sortOrder": "value-desc",
            "smallSegmentGrouping":{
              "enabled" : true,
                "value" : 2
            },
            "content": data[year]
        },

        callbacks: {
            onClickSegment: function (data) {
                department_clicked = data['data']['label'];
                document.getElementById('department_data').innerText = department_clicked;
                major_pie(major_data);
            }
        },
        "tooltips": {
            "enabled": true,
            "type": "placeholder",
            "string": "{label}: {value}, {percentage}%",
            styles: {
                fontSize:15
            }
	    }
    });

}

function major_pie(data) {
    major_data = data;
    if (major_pie_viz != null) {
        major_pie_viz.destroy();
        major_pie_viz = null;
    }
    major_pie_viz = new d3pie("pie1", {
        "size": {
            "canvasHeight": 375,
            "canvasWidth": 600,
            "pieOuterRadius": "90%"
        },
        data: {
            "sortOrder": "value-desc",
            "smallSegmentGrouping":{
              "enabled" : true,
                "value" : 1
            },
            "content": data[year][department_clicked]
        },
        "tooltips": {
            "enabled": true,
            "type": "placeholder",
            "string": "{label}: {value}, {percentage}%",
            styles: {
                fontSize:15
            }
	    },
        callbacks: {
            onClickSegment: function (data) {
                major = data['data']['label'];
                document.getElementById('major_data').innerText = major;
                document.getElementById('ethinicity_data').innerText = "Ethnicity for " + major ;
                document.getElementById('gender_data').innerText = "Gender for " + major ;
                ethinicity_line(ethinicity_data);
                gender_line(gender_data);
            }
        },
    });

}


function set_slider() {
    d3.select('#slider3').call(d3.slider()
            .axis(true).min(2004.5).max(2016).step(0.5)
        .on("slide", function(evt, value) {
            if(value % 1 != 0){
                year = 'fa' + value.toString().split('.')[0].slice(-2);
                if (department_data[year] === undefined) {
                    document.getElementById('year_data').innerText = "YEAR NOT FOUND : " + year;
                    document.getElementById('department_data').innerText = "";
                    document.getElementById('pie').innerText = "";
                    document.getElementById('pie1').innerText = "";
                    document.getElementById('ethinicity_data').innerText = "";
                    document.getElementById('ethnicity').innerText = "";
                    document.getElementById('gender_data').innerText = "";
                    document.getElementById('major_data').innerText = "";
                    document.getElementById('gender').innerText = "";
                }
                else {

                    department_pie(department_data);
                    major_pie(major_data);
                    department_clicked = "Engineering";
                    major = "Computer Science";
                    ethinicity_line(ethinicity_data);
                    gender_line(gender_data);
                    document.getElementById('department_data').innerText = department_clicked;
                    document.getElementById('ethinicity_data').innerText = "Ethnicity for " + major ;
                    document.getElementById('gender_data').innerText = "Gender for " + major ;
                    document.getElementById('major_data').innerText = "Computer Science";
                    document.getElementById('year_data').innerText = "Fall 20" + value.toString().split('.')[0].slice(-2);
                }
            }
            else{
                year = 'sp' + value.toString().split('.')[0].slice(-2);
                if (department_data[year] === undefined) {
                    document.getElementById('year_data').innerText = "YEAR NOT FOUND : " + year;
                }
                else {
                    department_pie(department_data);
                    major_pie(major_data);
                    department_clicked = "Engineering";
                    major = "Computer Science";
                    ethinicity_line(ethinicity_data);
                    gender_line(gender_data);
                    document.getElementById('department_data').innerText = department_clicked;
                    document.getElementById('ethinicity_data').innerText = "Ethnicity for " + major ;
                    document.getElementById('gender_data').innerText = "Gender for " + major ;
                    document.getElementById('major_data').innerText = "Computer Science";
                    document.getElementById('year_data').innerText = "Spring 20" + value.toString().split('.')[0].slice(-2);
                }

            }


        })


    );

}


// __________________________________________________________________________________________________________________________________________

function ethinicity_line(ethinicity) {
    ethinicity_data = ethinicity;

    
// Mike Bostock "margin conventions"
    var margin = {top: 20, right: 20, bottom: 30, left: 40},
        width = 600 - margin.left - margin.right,
        height = 600 - margin.top - margin.bottom;

// D3 scales = just math
// x is a function that transforms from "domain" (data) into "range" (usual pixels)
// domain gets set after the data loads
    var x = d3.scale.ordinal()
        .rangeRoundBands([0, width], .1);

    var y = d3.scale.linear()
        .range([height, 0]);

// D3 Axis - renders a d3 scale in SVG
    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    var tip = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-10, 0])
  .html(function(d) {

    return "<strong>" + d.label + " : " + " </strong> <span style='color:whitesmoke'>" + d.value + "</span>";
  });
    d3.select("#ethinicity_line").remove();
    var svg = d3.select("#ethnicity").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .attr("id", "ethinicity_line")
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")");

    svg.append("g")
        .attr("class", "y axis")
        .append("text") // just for the title (ticks are automatic)
        .attr("transform", "rotate(-90)") // rotate the text!
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Number of Students");

// d3.tsv is a wrapper around XMLHTTPRequest, returns array of arrays (?) for a TSV file
// type function transforms strings to numbers, dates, etc.
    replay(ethinicity_data[year][department_clicked][major]);
    function replay(data) {
        var slices = [];
        for (var i = 0; i < data.length; i++) {
            slices.push(data.slice(0, i + 1));
        }
        slices.forEach(function (slice, index) {
            setTimeout(function () {
                draw(slice);
            }, index * 300);
        });
    }

    function draw(data) {
        // measure the domain (for x, unique letters) (for y [0,maxFrequency])
        // now the scales are finished and usable
        x.domain(data.map(function (d) {
            return d.label;
        }));
        y.domain([0, d3.max(data, function (d) {
            return d.value;
        })]);

        // another g element, this time to move the origin to the bottom of the svg element
        // someSelection.call(thing) is roughly equivalent to thing(someSelection[i])
        //   for everything in the selection\
        // the end result is g populated with text and lines!
        svg.select('.x.axis').transition().duration(300).call(xAxis);

        // same for yAxis but with more transform and a title
        svg.select(".y.axis").transition().duration(300).call(yAxis);

        // THIS IS THE ACTUAL WORK!
        var bars = svg.selectAll(".bar").data(data, function (d) {
            svg.call(tip);
            return d.label;
        }); // (data) is an array/iterable thing, second argument is an ID generator function

        bars.exit()
            .transition()
            .duration(100)
            .attr("y", y(0))
            .attr("height", height - y(0))
            .style('fill-opacity', 1e-6)
            .remove();

        // data that needs DOM = enter() (a set/selection, not an event!)
        bars.enter().append("rect")
            .attr("class", "bar")
            .attr("y", y(0))
            .attr("height", height - y(0))
            .on('mouseover', tip.show)
            .on('mouseout', tip.hide);

        // the "UPDATE" set:
        bars.transition().duration(100).attr("x", function (d) {
            return x(d.label);
        }) // (d) is one item from the data array, x is the scale object from above
            .attr("width", x.rangeBand()) // constant, so no callback function(d) here
            .attr("y", function (d) {
                return y(d.value);
            })
            .attr("height", function (d) {
                return height - y(d.value);
            }); // flip the height, because y's domain is bottom up, but SVG renders top down

    }

}
//________________________________________________________________________________

function gender_line(gender) {
    gender_data = gender;


// Mike Bostock "margin conventions"
    var margin = {top: 20, right: 20, bottom: 30, left: 40},
        width = 600 - margin.left - margin.right,
        height = 600 - margin.top - margin.bottom;

// D3 scales = just math
// x is a function that transforms from "domain" (data) into "range" (usual pixels)
// domain gets set after the data loads
    var x = d3.scale.ordinal()
        .rangeRoundBands([0, width], .1);

    var y = d3.scale.linear()
        .range([height, 0]);

// D3 Axis - renders a d3 scale in SVG
    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    var tip = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-10, 0])
  .html(function(d) {

    return "<strong>" + d.label + " : " + " </strong> <span style='color:whitesmoke'>" + d.value + "</span>";
  });
    d3.select("#gender_line").remove();
    var svg = d3.select("#gender").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .attr("id", "gender_line")
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")");

    svg.append("g")
        .attr("class", "y axis")
        .append("text") // just for the title (ticks are automatic)
        .attr("transform", "rotate(-90)") // rotate the text!
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Number of Students");

// d3.tsv is a wrapper around XMLHTTPRequest, returns array of arrays (?) for a TSV file
// type function transforms strings to numbers, dates, etc.
    replay(gender_data[year][department_clicked][major]);
    function replay(data) {
        var slices = [];
        for (var i = 0; i < data.length; i++) {
            slices.push(data.slice(0, i + 1));
        }
        slices.forEach(function (slice, index) {
            setTimeout(function () {
                draw(slice);
            }, index * 300);
        });
    }

    function draw(data) {
        // measure the domain (for x, unique letters) (for y [0,maxFrequency])
        // now the scales are finished and usable
        x.domain(data.map(function (d) {
            return d.label;
        }));
        y.domain([0, d3.max(data, function (d) {
            return d.value;
        })]);

        // another g element, this time to move the origin to the bottom of the svg element
        // someSelection.call(thing) is roughly equivalent to thing(someSelection[i])
        //   for everything in the selection\
        // the end result is g populated with text and lines!
        svg.select('.x.axis').transition().duration(300).call(xAxis);

        // same for yAxis but with more transform and a title
        svg.select(".y.axis").transition().duration(300).call(yAxis);

        // THIS IS THE ACTUAL WORK!
        var bars = svg.selectAll(".bar").data(data, function (d) {
            svg.call(tip);
            return d.label;
        }); // (data) is an array/iterable thing, second argument is an ID generator function

        bars.exit()
            .transition()
            .duration(100)
            .attr("y", y(0))
            .attr("height", height - y(0))
            .style('fill-opacity', 1e-6)
            .remove();

        // data that needs DOM = enter() (a set/selection, not an event!)
        bars.enter().append("rect")
            .attr("class", "bar")
            .attr("y", y(0))
            .attr("height", height - y(0))
            .on('mouseover', tip.show)
            .on('mouseout', tip.hide);

        // the "UPDATE" set:
        bars.transition().duration(100).attr("x", function (d) {
            return x(d.label);
        }) // (d) is one item from the data array, x is the scale object from above
            .attr("width", x.rangeBand()) // constant, so no callback function(d) here
            .attr("y", function (d) {
                return y(d.value);
            })
            .attr("height", function (d) {
                return height - y(d.value);
            }); // flip the height, because y's domain is bottom up, but SVG renders top down

    }

}

