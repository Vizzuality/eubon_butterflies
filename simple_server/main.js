// Config file for carto
var request= {layers: [ {
    "user_name": "benlaken",
    "type": "cartodb",
    "options": {
      "sql": "Select * from processed",
      "cartocss": "#processed {raster-opacity:1; raster-scaling:near; raster-colorizer-default-mode:discrete; raster-colorizer-default-color:  transparent; raster-colorizer-epsilon:0.41; raster-colorizer-stops: stop(0, #ffffff) stop(1, #1767b6) stop(60, #2975ab)  stop(83, #75b1d3) stop(106, #b7dfe3) stop(129, #e7f5cb) stop(152, #ffe8a4) stop(175, #feba6e) stop(198, #ed6e43) stop(221, #d7191c)}",
      "cartocss_version": "2.3.0",
      "geom_column": "the_raster_webmercator",
      "geom_type": "raster",
      "raster_band": 1
    }}]};

var startVis = function() {


  var map = L.map('map', {scrollWheelZoom: true, center: [55,0], zoom: 4,});

  // adding basemap
  L.tileLayer('http://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png', {
      maxZoom: 18
  }).addTo(map, 1);



  // adding raster layer
  $.ajax({
    type: 'POST',
    dataType: 'json',
    contentType: 'application/json; charset=UTF-8',
    url: 'https://benlaken.carto.com/api/v1/map/',
    data: JSON.stringify(request),
    success: function(data) {
    console.log(data)
    var tileUrl = 'https://benlaken.carto.com/api/v1/map/' + data.layergroupid + '/{z}/{x}/{y}.png32';
    var utfGrid = 'https://benlaken.carto.com/api/v1/map/' + data.layergroupid + '/0/{z}/{x}/{y}.grid.json';
    L.tileLayer(tileUrl).addTo(map, 0);
  }
  });


  // adding query to grab butterfly observation points
  cartodb.createLayer(map, {user_name: 'benlaken', type: 'cartodb', sublayers: [{
                      legends: true,
                      sql: "SELECT * FROM butterfly_sightings  WHERE species = 1 AND year > 1999 AND year < 2004;",
                      cartocss: '#butterfly_sanitized {marker-width: 6; marker-fill: hsla(247, 90%, 52%, 1); marker-fill-opacity: 0.9;marker-allow-overlap: true;marker-line-width: 0.5; marker-line-color: #FFF; marker-line-opacity: 1;}'}]})
                      .addTo(map,1)
                      .done(function(layer){
                        //do stuff
                        console.log('legends active :'+ layer.options.legends);
                        console.log("Test Carto layers")
                      });


  cartodb.createLayer(map, {user_name: 'benlaken', type: 'cartodb', sublayers: [{
                      legends: true,
                      sql: "SELECT * FROM butterfly_sightings  WHERE species = 1 AND year > 2004 AND year < 2008;",
                      cartocss: '#butterfly_sanitized {marker-width: 6; marker-fill: hsla(283, 31%, 50%, 1); marker-fill-opacity: 0.9;marker-allow-overlap: true;marker-line-width: 0.5; marker-line-color: #FFF; marker-line-opacity: 1;}'}]})
                      .addTo(map,1)
                      .done(function(layer){
                        //do stuff
                        console.log('legends active :'+ layer.options.legends);
                        console.log("Test Carto layers")
                      });



};

window.onload = startVis;
