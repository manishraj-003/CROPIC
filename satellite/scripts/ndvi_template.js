// Google Earth Engine NDVI extraction template
// Replace AOI and export settings before execution.

var aoi = ee.Geometry.Rectangle([76.0, 29.0, 77.0, 30.0]);
var startDate = '2025-07-01';
var endDate = '2025-10-30';

var collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(aoi)
  .filterDate(startDate, endDate)
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20));

function addNDVI(image) {
  var ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI');
  return image.addBands(ndvi);
}

var withNdvi = collection.map(addNDVI);
var ndviMedian = withNdvi.select('NDVI').median().clip(aoi);

Export.image.toDrive({
  image: ndviMedian,
  description: 'cropic_ndvi_median',
  scale: 10,
  region: aoi,
  maxPixels: 1e13
});
