//function mapgenerate(data) {
//    var col = 'Murder per Unit Population';
//    var sliderValue = 1966;
//    var letter = 'Murder';
//
//    var div = d3.select("#mainWrapper");
//    var svg = div.append("svg")
//        .attr("id", "map13")
//        .attr("height", 500)
//        .attr("width", 960);
//
//
//    colorMapStart();
//    d3.select('#slider4').call(d3.slider().axis(true).min(1966).max(2012).step(1).on("slide", function (evt, value) {
//        var mapLetter = letterIs();
//        d3.select('#slider4text').text(value);
//        colorMap13(value, mapLetter);
//        sliderValue = value;
//    }));
//
//
//    function valueIs() {
//        console.log(sliderValue);
//        return sliderValue;
//    }
//
//    function letterIs() {
//        console.log('letter is: ' + letter);
//        return letter;
//    }
//
//    function colorMap13(sValue, z) {
//        var map;
//        var day_ = sValue;
//        var colorScheme = z;
//        if (colorScheme === 'Murder') {
//            map = d3.geomap.choropleth()
//                .geofile('../static/d3-geomap/topojson/countries/USA.json')
//                .colors(colorbrewer.Reds[9])
//                .projection(d3.geo.albersUsa)
//                .column(col)
//                .unitId('FIPS')
//                .scale(1000)
//                .legend(true);
//        }
//
//        var newD = [];
//        var dataArray = [];
//        var data = {
//        {
//            data | tojson | safe
//        }
//    }
//        ;
//        for (var i = 1965; i < 2013; i++) {
//            var newD = [];
//            for (var prop in data) {
//                if (data[prop].Year === i.toString()) {
//                    newD.push(data[prop]);
//                }
//            }
//            dataArray[i] = newD;
//        }
//        ;
//
//        d3.select("#map13")
//            .datum(dataArray[sliderValue])
//            .call(map.draw, map);
//    }
//
//    function colorMapStart() {
//        var map;
//        map = d3.geomap.choropleth()
//            .geofile('../static/d3-geomap/topojson/countries/USA.json')
//            .colors(colorbrewer.Reds[9])
//            .projection(d3.geo.albersUsa)
//            .column(col)
//            .unitId('FIPS')
//            .scale(1000)
//            .legend(true);
//        console.log(map);
//
//        var newD = [];
//        var dataArray = [];
//        var count = 0;
//    //    var data = {
//    //    {
//    //        data | tojson | safe
//    //    }
//    //}
//
//
//        for (var i = 1965; i < 2013; i++) {
//            var newD = [];
//            var count = 0;
//            for (var prop in data) {
//                if (data[prop].Year === i) {
//                    newD.push(data[prop]);
//                }
//            }
//            dataArray[i] = newD;
//        }
//        console.log(dataArray[1966]);
//        d3.select("#map13")
//            .datum(dataArray[1966])
//            .call(map.draw, map);
//        console.log(map);
//    }
//}