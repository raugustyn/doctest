var SelectedIndex = 0;
var FeaturesCount = 1415;
var reliefLinesSource;
var circlesSource;
var originsSource;
var wktFormat = new ol.format.WKT();
var animationTimeOut = undefined;

function startAnimation()
{
    stopAnimation();
    animationTimeOut = setInterval(
        function () {
            bounceToIndex("next");
        }, 10000);
}

function stopAnimation()
{
    if (animationTimeOut != undefined) {
        window.clearTimeout(animationTimeOut);
        animationTimeOut = undefined;
    }
}

function getWKTUrl(index)
{
    var url;
    if (index == "min") {
        url = "http://localhost/TB04CUZK001/CartoModel/workflow/rest/getfeature.py?profile=Propustky&index=min";
        console.log(url);
        testUrl = "http://localhost:63342/TB04CUZK001_CartoModel/workflow/web/testdata/propustky_01.wkt";
    }
    else if (index == "max") {
        url = "http://localhost/TB04CUZK001/CartoModel/workflow/rest/getfeature.py?profile=Propustky&index=max";
        console.log(url);
        testUrl = "http://localhost:63342/TB04CUZK001_CartoModel/workflow/web/testdata/propustky_02.wkt";
    }
    else if (index == "next") {
        url = "http://localhost/TB04CUZK001/CartoModel/workflow/rest/getfeature.py?profile=Propustky&index=" + SelectedIndex.toString() + "&operator=greatherthan";
        testUrl = "http://localhost:63342/TB04CUZK001_CartoModel/workflow/web/testdata/propustky_02.wkt";
    }

    console.log(url);
    if (true) {
        return url
    }
    else {
        return testUrl
    }
}

var overlayStyle = (function() {
  var styles = {};
  styles['Polygon'] = [
    new ol.style.Style({
      fill: new ol.style.Fill({
        color: [255, 255, 255, 0.5]
      })
    }),
    new ol.style.Style({
      stroke: new ol.style.Stroke({
        color: [255, 255, 255, 1],
        width: 5
      })
    }),
    new ol.style.Style({
      stroke: new ol.style.Stroke({
        color: [0, 153, 255, 1],
        width: 3
      })
    })
  ];
  styles['MultiPolygon'] = styles['Polygon'];

  styles['LineString'] = [
    new ol.style.Style({
      stroke: new ol.style.Stroke({
        color: [0, 0, 0, 1],
        width: 5
      })
    }),
    new ol.style.Style({
      stroke: new ol.style.Stroke({
        color: [255, 255, 128, 1],
        width: 3
      })
    }),
    new ol.style.Style({
        image: new ol.style.RegularShape({
            fill: new ol.style.Fill({color: 'rgba(255, 255, 255, 0.2)'}),
            stroke: new ol.style.Stroke({ color: "#ff0000", width: 2 }),
            points: 4,
            radius: 5,
            angle: Math.PI / 4
        }),
        geometry: function(feature) {
            var coords = feature.getGeometry().getCoordinates();
            return new ol.geom.MultiPoint([coords[0]]); //, coords[coords.length - 1]]);
        }
    })
  ];
  styles['MultiLineString'] = styles['LineString'];

  styles['Point'] = [
    new ol.style.Style({
      image: new ol.style.Circle({
        radius: 7,
        fill: new ol.style.Fill({
          color: [0, 153, 255, 1]
        }),
        stroke: new ol.style.Stroke({
          color: [255, 255, 255, 0.75],
          width: 1.5
        })
      }),
      zIndex: 100000
    })
  ];
  styles['MultiPoint'] = styles['Point'];

  styles['GeometryCollection'] = styles['Polygon'].concat(styles['Point']);

  return function(feature, resolution) {
    return styles[feature.getGeometry().getType()];
  };
})();

var layerInfos = [];
var select = new ol.interaction.Select({
  style: overlayStyle
});
var modify = new ol.interaction.Modify({
  features: select.getFeatures(),
  style: overlayStyle
});

/** SELECT */

var TRAILCOLOR = "#6e6e6e";
var trailStylesInfo = [
    { ZNACKA: "2490101", strokeWidth: 1.5, dashes:[15, 10] },
    { ZNACKA: "2480001", strokeWidth: 3.2, dashes:[43, 11] },
    { ZNACKA: "2480006", strokeWidth: 3.2, dashes:[33, 8.5] },
    { ZNACKA: "2470000", strokeWidth: 1.5, dashes:[15, 10] },
    { ZNACKA: "2490200", strokes:[3.5, 6], dashes:null}
]

/** @type {ol.style.Circle } **/
var image = new ol.style.Circle({ radius: 5, fill: null, stroke: new ol.style.Stroke({color: 'red', width: 1}) });

/** @type {ol.style.Stroke} **/
var dynamicStroke = new ol.style.Stroke({ color: 'green', width: 1 });

var styles = {
  'Point': [new ol.style.Style({ image: image })],
  'LineString': [new ol.style.Style({ stroke: dynamicStroke })],
  'MultiLineString': [new ol.style.Style({ stroke: dynamicStroke })],
  'MultiPoint': [new ol.style.Style({image: image })],
  'MultiPolygon': [new ol.style.Style({ stroke: dynamicStroke, fill: new ol.style.Fill({ color: 'rgba(255, 255, 0, 0.1)' }) })],
  'Polygon': [new ol.style.Style({ stroke: dynamicStroke, fill: new ol.style.Fill({ color: 'rgba(0, 0, 255, 0.1)' })})],
  'GeometryCollection': [new ol.style.Style({ stroke: dynamicStroke, fill: new ol.style.Fill({ color: 'magenta' }), image: new ol.style.Circle({ radius: 10, fill: null, stroke: dynamicStroke }) })],
  'Circle': [new ol.style.Style({ stroke: dynamicStroke, fill: new ol.style.Fill({ color: 'rgba(255,0,0,0.2)' })})]
};

var styleFunction = function(feature, resolution) {
    var newWidth = Math.round(2/resolution);
    //console.log(feature.getGeometry().getType() + ":" + resolution + ":" + newWidth);
    var properties = feature.getProperties();
    var dash = dynamicStroke.getLineDash();
    var handled = false;
    for (var index in trailStylesInfo) {
        trailStyleInfo = trailStylesInfo[index];
        if (trailStylesInfo.ZNACKA == properties["ZNACKA"]) {
            if (trailStylesInfo.dashes != null) {
                dynamicStroke.setLineDash([20, 15]);
            }
        }
    }
    if (properties["ZNACKA"] = "2490101") {
        dynamicStroke.setLineDash([20, 15]);
    }
    else {
        dynamicStroke.setLineDash(null);
    }
    dynamicStroke.setWidth(newWidth);
    return styles[feature.getGeometry().getType()];
};

/** @type {ol.Extent} */
var projectExtent = [-640095.5327659437898546,-1042961.2575031011365354, -638877.1240791263990104,-1042267.5186156239360571];

// END OF PROJECT EXTENT

/** @type {Array.<ol.style.Style>} */
function getRichStyles(strokeColor, strokeWidth)
{
    var result = [
    new ol.style.Style({ stroke: new ol.style.Stroke({ color: strokeColor, width: strokeWidth }) }),
    new ol.style.Style({
        image: new ol.style.RegularShape({
            fill: new ol.style.Fill({color: 'rgba(255, 255, 255, 0.2)'}),
            stroke: new ol.style.Stroke({ color: strokeColor, width: 2 }),
            points: 4,
            radius: 5,
            angle: Math.PI / 4
        }),
        geometry: function(feature) {
            var coords = feature.getGeometry().getCoordinates();
            return new ol.geom.MultiPoint([coords[0]]); //, coords[coords.length - 1]]);
        }
    }),
    new ol.style.Style({
        image: new ol.style.Circle({ radius: 5, fill: new ol.style.Fill({color: 'rgba(255, 255, 255, 0.2)'}), stroke: new ol.style.Stroke({ color: strokeColor, width: 2 }) }),
        geometry: function(feature) {
            var coords = feature.getGeometry().getCoordinates();
            return new ol.geom.MultiPoint(coords.slice(1, coords.length - 1));
        }
    })];
    return result;
}

var VectorLayerInfos = [
    { name: "shape", layer: undefined, visible: true, styles: getRichStyles('green', 3) },
    { name: "circle", layer: undefined, visible: true, styles: getRichStyles('green', 3) },
    { name: "origin",  layer: undefined, visible: true, styles: getRichStyles('green', 3) }
    //{ url: 'data/01_Paralelizace/Shot_01/Z_TerenniRelief_L.geojson', name: 'Terénní stupně', layer: undefined, styles: getRichStyles('green', 3), visible: true },
    //{ url: 'data/Index/Z_KomRuzna_L.geojson', name: 'cesty', layer: undefined, styles: getRichStyles('#ff0066', 3) }
];

/** @type {String} **/
var VectorCheckBoxPrefix = "VectorCheckBox_";

/**
 * @type {ol.layer.Image}
 */
var SampleImageLayer = new ol.layer.Image({
    visible: false,
    source: new ol.source.ImageStatic({
        // STATIC IMAGE URL
        url: 'Data/Index/situace2_zm10_gen.png',
        // END OF STATIC IMAGE URL
        imageExtent: projectExtent,
        imageSize: [5866, 3088]
    })
});

/** @type {Array.Object} */
var backgroundLayers = [
    { controlId: "zm10",     wmsURL: 'http://geoportal.cuzk.cz/WMS_ZM10_PUB/WMService.aspx',     wmsLayerNames: 'GR_ZM10',       layer : null},
    { controlId: "zm25",     wmsURL: 'http://geoportal.cuzk.cz/WMS_ZM25_PUB/WMService.aspx',     wmsLayerNames: 'GR_ZM25',       layer : null},
    { controlId: "ortofoto", wmsURL: 'http://geoportal.cuzk.cz/WMS_ORTOFOTO_PUB/WMService.aspx', wmsLayerNames: 'GR_ORTFOTORGB', layer : null}
]

/** @type {Array.ol.layer} **/
var layers = [];

function initBackgroundLayers()
{
    for (var i in backgroundLayers) {
        var info = backgroundLayers[i];
        info.layer = new ol.layer.Tile({
            visible: info.controlId == "",
            extent: [-906000, -1228000, -430000, -933999],
            source: new ol.source.TileWMS({
                url: info.wmsURL,
                params: {'LAYERS': info.wmsLayerNames},
                serverType: 'geoserver'
            })
        });
        layers.push(info.layer);
        layerInfos.push({controlId:info.controlId , layer: info.layer});
    }
}

function getVectorLayerCheckboxId(index)
{
    return VectorCheckBoxPrefix + index;
}

var view = undefined;
var targetSource;

function getFirstFeatureCoordinates(source)
{
    var features = source.getFeatures();
    var feature = features[0];
    var geometry = feature.getGeometry();
    var coordinates = geometry.getCoordinates();
    return coordinates;
}

var inputCoordinates = undefined;
var targetCoordinates = undefined;

function operationStageChangeProc(value)
{
    //console.log("operationStageChangeProc(" + value + ")");

    if (inputCoordinates == undefined) {
        inputCoordinates = getFirstFeatureCoordinates(VectorLayerInfos[2].layer.getSource());
    }

    if (targetCoordinates == undefined) {
        targetCoordinates = getFirstFeatureCoordinates(VectorLayerInfos[3].layer.getSource());
    }

    VectorLayerInfos[2].layer.setVisible(false);
    VectorLayerInfos[3].layer.setVisible(false);

    reliefSource = VectorLayerInfos[0].layer.getSource();

    var features = reliefSource.getFeatures();
    var feature = features[0];
    var geometry = feature.getGeometry();
    var coordinates = geometry.getCoordinates();
    var newCoordinate;
    for (var coordinateIndex=0; coordinateIndex < coordinates.length; coordinateIndex++) {
        if (coordinateIndex < value) {
            newCoordinate = targetCoordinates[coordinateIndex]
        }
        else {
            newCoordinate = inputCoordinates[coordinateIndex]
        }
        coordinate = coordinates[coordinateIndex];
        coordinate[0] = newCoordinate[0];
        coordinate[1] = newCoordinate[1];
    }

    geometry.setCoordinates(coordinates);
}

function getCenterPoint(feature)
{
    return ol.extent.getCenter(feature.getGeometry().getExtent());
}

function addFeature(source, wkt) {
    if (wkt != "") {
        var feature = wktFormat.readFeature(wkt, {dataProjection: 'EPSG:5514', featureProjection: 'EPSG:5514'});
        source.addFeature(feature);

        return feature;
    }
    else return undefined;
}

function bounceToIndex(index)
{
    reliefLinesSource.clear();
    circlesSource.clear();
    originsSource.clear();

    $.get(getWKTUrl(index), function (data) {
        if (data != "") {
            var dataJSON = JSON.parse(data);
            addFeature(circlesSource, dataJSON.centerLine);
            addFeature(reliefLinesSource, dataJSON.edge);

            feature = addFeature(originsSource, dataJSON.wkt);
            SelectedIndex = dataJSON.ogc_fid;

            document.getElementById("FeatureIndexInput").value = SelectedIndex.toString();
            if (feature != undefined) {
                var centerPoint = getCenterPoint(feature);
                bounceToCoordinates(centerPoint);
            }
        }
    });
}

function bounceToCoordinates(coordinates)
{
    var duration = 2000;
    var start = +new Date();
    var pan = ol.animation.pan({
                    duration: duration,
                    source: /** @type {ol.Coordinate} */ (view.getCenter()),
                    start: start
                });
    var bounce = ol.animation.bounce({
            duration: duration,
            resolution: 4 * view.getResolution(),
            start: start
        });
    //map.beforeRender(pan, bounce);
    view.setCenter(coordinates);
}

/**
 * main function - initialize the map application
 * @type {function}
 */
var main = function()
{
    proj4.defs('EPSG:5514', '+proj=krovak +lat_0=49.5 +lon_0=24.83333333333333 +alpha=30.28813972222222 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +towgs84=570.8,85.7,462.8,4.998,1.587,5.261,3.56 +units=m +no_defs');

    var resolutions = [131088, 65544, 32772, 16386, 8193, 4096.5, 2048.25, 1024.125, 512.0625, 256.03125, 128.015625, 64.0078125, 32.00390625, 16.001953125, 8.0009765625,
                        4.00048828125, 2.000244140625, 1.0001220703125, 0.50006103515625, 0.250030517578125, 0.1250152587890625, 0.06250762939453125];

    var center = [(projectExtent[0] - (projectExtent[0] - projectExtent[2]) / 2), (projectExtent[1] - (projectExtent[1] - projectExtent[3]) / 2)];

    var krovakProjection = new ol.proj.Projection({code: 'EPSG:5514'});

    initBackgroundLayers();
    layers.push(SampleImageLayer);
    layerInfos.push({controlId:"overlay" , layer: SampleImageLayer});

    var createAndAddSource = function(layerIndex, styles) {
        var resultSource = new ol.source.Vector({features: []});
        var resultVector = new ol.layer.Vector({source: resultSource /*, style: [styles[0]] */});
        layers.push(resultVector);

        VectorLayerInfos[layerIndex].layer = resultVector;
        return resultSource;
    };

    var targetVector;

    reliefLinesSource  = createAndAddSource(0, getRichStyles('green', 3));
    circlesSource = createAndAddSource(1, getRichStyles('green', 3));
    originsSource = createAndAddSource(2, getRichStyles('green', 3));

    for (var i in VectorLayerInfos) {
        var info = VectorLayerInfos[i];
        layers.push(info.layer);
        layerInfos.push({controlId:getVectorLayerCheckboxId(i) , layer: SampleImageLayer});
    }

    targetSource = new ol.source.Vector({
                projection: krovakProjection,
                url: 'data/01_Paralelizace/Shot_02/Z_TerenniRelief_L.geojson',
                format: new ol.format.GeoJSON({defaultDataProjection: krovakProjection})
            });

    view = new ol.View({
            resolutions: resolutions,
            projection: krovakProjection,
            center: center,
            zoom: 19
        });
    map = new ol.Map({
        interactions: ol.interaction.defaults().extend([select, modify]),
        target: 'mapdiv',
        layers: layers,
        view: view
    });


    createVectorLayerCheckboxes();
    $(map.getViewport()).on('mousemove', null, {map: map}, mouseMoveHandler);
    $(map.getViewport()).on('mouseout', null, null, mouseOutHandler);
    $(map.getViewport()).on('mousedown', null, {map: map}, mouseDownHandler);

    initControllers();
};

function switchLayerVisibility(evt)
{
    var checkbox = evt.target;
    for (var index in layerInfos) {
        var layerInfo = layerInfos[index];
        if (layerInfo.controlId == checkbox.id) {
            layerInfo.layer.setVisible(checkbox.checked);
        }
    }
}

function createVectorLayerCheckboxes()
{
    var layersDiv = document.getElementById("VectorLayers");
    html = "";
    for (var i in VectorLayerInfos) {
        var info = VectorLayerInfos[i];
        if (info.visible) {
            var id = getVectorLayerCheckboxId(i);
            html += '<input id="' + id + '" type="checkbox" name="' + id + '" onclick="switchVectorLayer(this)" checked>&nbsp;' + info.name + '<br>';
        }
    }
    layersDiv.innerHTML = html;
}

function switchVectorLayer(checkbox)
{
    var index = parseInt(checkbox.id.substring(VectorCheckBoxPrefix.length));
    VectorLayerInfos[index].layer.setVisible(checkbox.checked);
}

/**
 * mouse move handler - display feature info
 * @param {Event} evt
 */
var mouseMoveHandler = function(evt) {
    var map = evt.data.map;
    var mousePosition = map.getEventPixel(evt.originalEvent);

    var displayAttributes = function(feature, layer) {
        var html = '<strong>' + (layer.get('name') || 'Vrstva beze jména') + '</strong>\n';
        var properties = feature.getProperties();
        for (var attr in properties)
            if (["geometry", "ZDROJ_ID", "SHAPE_Leng"].indexOf(attr) == -1) {
                html += '<br>\n' + attr + ': ' + String(properties[attr]);
            }
        $('#info').html(html);
    };

    $('#info').innerHTML = '&nbsp;hh';
    map.forEachFeatureAtPixel(mousePosition, displayAttributes);
};

/**
 * mouse down handler - display feature info
 * @param {Event} evt
 */
var mouseDownHandler = function(evt) {
    var map = evt.data.map;
    var mousePosition = map.getEventPixel(evt.originalEvent);

    var displayAttributes = function(feature, layer) {
        var html = '<strong>' + (layer.get('name') || 'Vrstva beze jména') + '</strong>\n';
        var properties = feature.getProperties();
        for (var attr in properties) {
            html += '<br>\n' + attr + ': ' + String(properties[attr]);
        }

        $('#StaticInfo').html(html);
    };

    $('#info').innerHTML = '&nbsp;hh';
    map.forEachFeatureAtPixel(mousePosition, displayAttributes);
};

/**
 * mouse ount handler
 * @param {Event} evt
 */
var mouseOutHandler = function(evt) { $('#info').html(''); };

/**
 * initialize input and button controllers
 * @type {function}
 */
var initControllers = function() {
    $('#NoBackground')[0].onclick = switchBackgroundHandler;
    for (var index in backgroundLayers) {
        $('#' + backgroundLayers[index].controlId)[0].onclick = switchBackgroundHandler;
    }

    /*
    $('#overlay')[0].onclick = function(evt) {
        var checkbox = evt.target;
        if (checkbox.name == 'imageOverlay') {
            SampleImageLayer.setVisible(checkbox.checked);
        }
    };
    */

    $('#SwitchShowVertexes')[0].onclick = function(evt) {
        var checkbox = evt.target;
        for (var index in VectorLayerInfos) {
            var info = VectorLayerInfos[index];
            var NewStyle = checkbox.checked ? info.styles : [info.styles[0]];
            info.layer.setStyle(NewStyle);
        }
    };

    $('#SwitchVectors')[0].onclick = function(evt) {
        var checkbox = evt.target;
        for (var index in VectorLayerInfos) {
            VectorLayerInfos[index].layer.setVisible(checkbox.checked);
        }
    };
};

/**
 * handle background layer switcher
 * @type {function}
 * @param {MouseEvent} evt
 */
var switchBackgroundHandler = function(evt)
{
    switchedControlId = $('input:radio[name=background]:checked').val();
    for (var index in backgroundLayers) {
        var layerInfo = backgroundLayers[index];
        layerInfo.layer.setVisible(switchedControlId == layerInfo.controlId);
    }
};

/** init */
main();