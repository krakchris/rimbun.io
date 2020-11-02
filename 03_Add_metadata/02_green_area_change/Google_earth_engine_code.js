// This script can be used to add vegetatoin change data to water polygons for the rimbun.io project
//
// A large part of the code is based on the example script on classification: 
// https://code.earthengine.google.com/30ea4c1a33043de7e7a64ebd854fa32e 
//
// workflow Short: 
// 1. Create city geometry using "get_city_outline.ipynb" notebook
//    Upload shapefile under Assets > NEW > Shape Files (only .shp, .shx, .prj, .dbf files)
//    After succesful ingestion select 'import into script'
//    Name the Table "city"               
// 2. Check if there is LANDSAT data available in the AOI
//   - if there is no data then the analysis cannot be run
// 3. Create training data by selecting areas that are stable over the years using Geometry Imports > new layer (top left of map in gee code editor) 
//     -rename the separate geometries to:
//       - Urban, Vegetation, and Water
// 4. Run the analysis by pressing 'Run' (top center right in gee code editor) or Ctrl - Enter.
// 5. Verify the quality of the classification by visual inspection and study the confusion matrix
// 6. In case of acceptable results set "export_training_data" to "true" and export the training data to drive
// 7. Switch to jupyter notebook to add landcover change to water delineation data

// Optional:
// - Export classifications to your drive. By selecting 'RUN' and selecting output method. 
// - Download and open the .tif files with your favorite GIS software, plot with R or python
//
//
// By: Jim Groot & Chris van Diemen


// define parameters /////////////////////////////////////////////////////
var city_name = 'Jakarta'

// first create training data and verify quality in code editor then export training data 
var export_training_data = false;

// optional, export classification images to drive for visualizations
var export_classifications = false;

// import assets ////////////////////////////////////////////////////////

var geometry = ee.FeatureCollection(city);

print(city)

// define functions /////////////////////////////////////////////////////
// pad function
function pad(n, width, z) {
  z = z || '0';
  n = n + '';
  return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}


/**
 * Function to mask clouds based on the pixel_qa band of Landsat SR data.
 * @param {ee.Image} image Input Landsat SR image
 * @return {ee.Image} Cloudmasked Landsat image
 */
var cloudMaskL457 = function(image) {
  var qa = image.select('pixel_qa');
  // If the cloud bit (5) is set and the cloud confidence (7) is high
  // or the cloud shadow bit is set (3), then it's a bad pixel.
  var cloud = qa.bitwiseAnd(1 << 5)
                  .and(qa.bitwiseAnd(1 << 7))
                  .or(qa.bitwiseAnd(1 << 3));
  // Remove edge pixels that don't occur in all bands
  var mask2 = image.mask().reduce(ee.Reducer.min());
  return image.updateMask(cloud.not()).updateMask(mask2);
};

//functions for Indices
var addNDVI = function(image) {
  var ndvi = image.normalizedDifference(['B4', 'B3']).rename('NDVI');
  return image.addBands(ndvi);
};

var addindex = function(image) {
  var ndvi = image.normalizedDifference(['B4', 'B3']).rename('NDVI');
  var ndwi = image.normalizedDifference(['B2', 'B5']).rename('NDWI');
  return image.addBands(ndvi).addBands(ndwi);
};

// Import GEE data /////////////////////////////////////////////////////

var LS5 = ee.ImageCollection('LANDSAT/LT05/C01/T1_SR')
  // .filter(ee.Filter.bounds(geometry))
  .filterDate('1986-01-01', '2000-12-31');
  
var LE7 = ee.ImageCollection('LANDSAT/LE07/C01/T1_SR')
  // .filter(ee.Filter.bounds(geometry))
  .filterDate('2001-01-01', '2018-12-31');

var LS5NDVI = LS5.map(addNDVI);
var LE7NDVI = LE7.map(addNDVI);

// Select date ranges and apply cloud filters
// (note: we have all ranges separately here to enable easy adjustments to specific year ranges 
// in case the data for a specific year exhibits extreme artifacts. This approach allows for 
// the application of suitable fixes. Not the most beautiful code. 
// Find two examples of data selection below.)

// use the following template to select the mean value for landsat in the date range:
//var y0 = LS5NDVI.filterDate('1984-01-01', '1987-12-31').map(cloudMaskL457).mean().clip(geometry);

// use the following template to select the greenes pixel (e.g. select NDVI as quality measure)
// var y1 = LS5NDVI.filterDate('1988-01-01', '1989-12-31').map(cloudMaskL457).qualityMosaic('NDVI').clip(geometry);

var y1 = LS5NDVI.filterDate('1988-01-01', '1989-12-31').map(cloudMaskL457).mean().set('system:time_start', '1989');
var y2 = LS5NDVI.filterDate('1990-01-01', '1991-12-31').map(cloudMaskL457).mean().set('system:time_start', '1991');
var y3 = LS5NDVI.filterDate('1992-01-01', '1993-12-31').map(cloudMaskL457).mean().set('system:time_start', '1993');
var y4 = LS5NDVI.filterDate('1994-01-01', '1995-12-31').map(cloudMaskL457).mean().set('system:time_start', '1995');
var y5 = LS5NDVI.filterDate('1996-01-01', '1997-12-31').map(cloudMaskL457).mean().set('system:time_start', '1997');
var y6 = LS5NDVI.filterDate('1998-01-01', '1999-12-31').map(cloudMaskL457).mean().set('system:time_start', '1999');   
var y7 = LE7NDVI.filterDate('2000-01-01', '2001-12-31').map(cloudMaskL457).mean().set('system:time_start', '2001');
var y8 = LE7NDVI.filterDate('2002-01-01', '2003-12-31').map(cloudMaskL457).mean().set('system:time_start', '2003');
var y9 = LE7NDVI.filterDate('2004-01-01', '2005-12-31').map(cloudMaskL457).mean().set('system:time_start', '2005');
var y10 = LE7NDVI.filterDate('2006-01-01', '2007-12-31').map(cloudMaskL457).mean().set('system:time_start', '2007');
var y11 = LE7NDVI.filterDate('2008-01-01', '2009-12-31').map(cloudMaskL457).mean().set('system:time_start', '2009');
var y12 = LE7NDVI.filterDate('2010-01-01', '2011-12-31').map(cloudMaskL457).mean().set('system:time_start', '2011');
var y13 = LE7NDVI.filterDate('2012-01-01', '2013-12-31').map(cloudMaskL457).mean().set('system:time_start', '2013');
var y14 = LE7NDVI.filterDate('2014-01-01', '2015-12-31').map(cloudMaskL457).mean().set('system:time_start', '2015');   
var y15 = LE7NDVI.filterDate('2016-01-01', '2018-12-31').map(cloudMaskL457).mean().set('system:time_start', '2018');
var y16 = LE7NDVI.filterDate('2019-01-01', '2020-06-04').map(cloudMaskL457).mean().set('system:time_start', '2020');

//add indices (NDVI / NDWI, see functions) 
var y1 = addindex(y1);
var y2 = addindex(y2);
var y3 = addindex(y3);
var y4 = addindex(y4);
var y5 = addindex(y5);
var y6 = addindex(y6);
var y7 = addindex(y7);
var y8 = addindex(y8);
var y9 = addindex(y9);
var y10 = addindex(y10);
var y11 = addindex(y11);
var y12 = addindex(y12);
var y13 = addindex(y13);
var y14 = addindex(y14);
var y15 = addindex(y15);

// Create classifications /////////////////////////////////////////////////////

// 1. select polygons 
// 2. generate random points in polygons
// 3. use random points in training algorithm
// 4. use trained classifier to predict classes for all pixels

// create random points and add class using polgyons
var addpoints = function(feature, Class) {
  var addclass = function(feature) {
  return feature.set({landuse: Class });
  };
  var trainpoints = ee.FeatureCollection.randomPoints(feature,1000,0);
  var trainset = trainpoints.map(addclass)
  return trainset
};

// use the polygon data to create random training points
var urban = addpoints(Urban,1);
var water = addpoints(Water,2);
var vegetation = addpoints(Vegetation,3);

// Merge the three geometry layers into a single FeatureCollection.
var newfc = urban.merge(vegetation).merge(water);
print (newfc)
// Use these bands for classification.
var bands = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'NDVI','NDWI'];
// The name of the property on the points storing the class label.
var classProperty = 'landuse';

// Function to create a Make a Random Forest classifier and train it
// given data from a specific year. 
var buildClassifier = function(range_data, bands, newfc, classProperty) {
  
  // Sample the composite to generate training data.  Note that the
  // class label is stored in the 'landcover' property. 
  var training_data = range_data.select(bands).sampleRegions({
    collection: newfc,
    properties: [classProperty],
    scale: 30
  });
  
  // Make a Random Forest classifier and train it
  var classifier = ee.Classifier.randomForest(10)
  .train(training_data, 'landuse');
  
    return classifier
};

// Classify the composite, use function to create a separate classifier for each year. 
var classified1 = y1.classify(buildClassifier(y1, bands, newfc, classProperty)).set('system:time_start', '1989');
var classified2 = y2.classify(buildClassifier(y2, bands, newfc, classProperty)).set('system:time_start', '1991');
var classified3 = y3.classify(buildClassifier(y3, bands, newfc, classProperty)).set('system:time_start', '1993');
var classified4 = y4.classify(buildClassifier(y4, bands, newfc, classProperty)).set('system:time_start', '1995')
var classified5 = y5.classify(buildClassifier(y5, bands, newfc, classProperty)).set('system:time_start', '1997');
var classified6 = y6.classify(buildClassifier(y6, bands, newfc, classProperty)).set('system:time_start', '1999');
var classified7 = y7.classify(buildClassifier(y7, bands, newfc, classProperty)).set('system:time_start', '2001');
var classified8 = y8.classify(buildClassifier(y8, bands, newfc, classProperty)).set('system:time_start', '2003');
var classified9 = y9.classify(buildClassifier(y9, bands, newfc, classProperty)).set('system:time_start', '2005');
var classified10 = y10.classify(buildClassifier(y10, bands, newfc, classProperty)).set('system:time_start', '2007');
var classified11 = y11.classify(buildClassifier(y11, bands, newfc, classProperty)).set('system:time_start', '2009');
var classified12 = y12.classify(buildClassifier(y12, bands, newfc, classProperty)).set('system:time_start', '2011');
var classified13 = y13.classify(buildClassifier(y13, bands, newfc, classProperty)).set('system:time_start', '2013');
var classified14 = y14.classify(buildClassifier(y14, bands, newfc, classProperty)).set('system:time_start', '2015');
var classified15 = y15.classify(buildClassifier(y15, bands, newfc, classProperty)).set('system:time_start', '2017');



var band_classes = function(classified){
  
  var area = ee.Image.pixelArea();
  
  // create separate bands for counting classifications
  var classified_urban_band = classified.eq(1);
  var classified_urban_water = classified.eq(2);
  var classified_urban_veg = classified.eq(3);
  
  // rename bands for later selection
  var class_urban_band_rename = classified_urban_band.rename('class_urban');
  var class_water_band_rename = classified_urban_water.rename('class_water');
  var class_veg_band_rename = classified_urban_veg.rename('class_veg');
  
  // calculate area
  var urbanArea = class_urban_band_rename.multiply(area).divide(1000000).rename('urbanArea');
  var waterArea = class_water_band_rename.multiply(area).divide(1000000).rename('waterArea');
  var vegArea = class_veg_band_rename.multiply(area).divide(1000000).rename('vegArea');
  
  // add bands to image
  var image_out_u = classified.addBands(urbanArea);
  var image_out_uw = image_out_u.addBands(waterArea);
  var image_out_uwv = image_out_uw.addBands(vegArea);
  
  // print(image_out_uwv)

  return image_out_uwv.select(['urbanArea', 'vegArea']);
}

// Get accuracy assessment 
print(buildClassifier(y15, bands, newfc, classProperty).confusionMatrix())


// Export classifications /////////////////////////////////////////////////////

// Export classified images 
var classified_collection = [classified1, classified2, 
classified3, classified4, classified5, classified6, classified7, 
classified8, classified9, classified10, classified11, classified12, 
classified13, classified14, classified15]

var count_classes = classified_collection.map(band_classes)

var chart_timeseries = ui.Chart.image.series(
  count_classes, 
  geometry, 
  ee.Reducer.sum(), 
  100);

print(chart_timeseries);



// Visualize results /////////////////////////////////////////////////////

// define visualization parameters for visual check of data
var visParams = {
  bands: ['B3', 'B2', 'B1'],
  min: 0,
  max: 3000,
  gamma: 1.4,
};

// add some landsat imagers to map
Map.addLayer(y1.clip(geometry), visParams,'y1 Landsat');
Map.addLayer(y15.clip(geometry), visParams,'y15 Landsat');

// Visualize some of the classified layers
Map.addLayer(classified1.clip(geometry), {min: 1, max: 3, palette: ['grey', 'blue', 'green']}, '1988 Classification');
Map.addLayer(classified15.clip(geometry), {min: 1, max: 3, palette: ['grey', 'blue', 'green']}, '2018 Classification');

Map.centerObject(city);



// function to export training data to drive
if (export_training_data){

// Export the FeatureCollection.
Export.table.toDrive({
  collection: Water,
  description: 'water_trainingdata_export',
  fileFormat: 'GeoJSON'
});

Export.table.toDrive({
  collection: Urban,
  description: 'urban_trainingdata_export',
  fileFormat: 'GeoJSON'
});

Export.table.toDrive({
  collection: Vegetation,
  description: 'vegetation_trainingdata_export',
  fileFormat: 'GeoJSON'
});

}

// function to export classification rasters to drive
if(export_classifications){

var i;

for (i = 0; i <= classified_collection.length; i++) {
  Export.image.toDrive({
  image: classified_collection[i],
  description: 'Classified_'+ city_name + "_" + pad(i.toString(), 2),
  scale: 30,
  region: geometry
  });
}

}