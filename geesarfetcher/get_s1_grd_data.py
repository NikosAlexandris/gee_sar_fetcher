# constants
SENTINEL1_COLLECTION_ID = 'COPERNICUS/S1_GRD'
VV = 'VV'
VH = 'VH'
IW = 'IW'
ASCENDING = 'ASCENDING'
DESCENDING = 'DESCENDING'

# imports
import ee
ee.Initialize()
import datetime

# Quick Example

# where?
scale=1000
crs = 'SR-ORG:6974'  # projection
top_left = [-104.77431630331856, 41.829889598264826]
bottom_right = [-104.65140675742012, 41.81515375846025]
# top_left = [5.26948161, 49.97440374]
# bottom_right = [8.07913236, 47.90621773]
x_min = top_left[0]
y_min = bottom_right[1]
x_max = bottom_right[0]
y_max = top_left[1]
extent = (x_min, y_min, x_max, y_max)
# geometry = ee.Geometry.Rectangle(extent, crs, False)
geometry = ee.Geometry.Rectangle(extent)

# when?
start_date = datetime.datetime(2019, 6, 1)
end_date = datetime.datetime(2019, 6, 10)

# orbit properties
pass_direction = ASCENDING

# filter
image_collection = (ee.ImageCollection(SENTINEL1_COLLECTION_ID)
          .filter(ee.Filter.date(start_date, end_date))
          .filterBounds(geometry)
          .filter(ee.Filter.listContains('transmitterReceiverPolarisation', VV))
          .filter(ee.Filter.listContains('transmitterReceiverPolarisation', VH))
          .filter(ee.Filter.eq('instrumentMode', IW))
          .filter(ee.Filter.eq('orbitProperties_pass', pass_direction))
          .filter(ee.Filter.eq('resolution_meters', 10))
)

# aggregate
statistic = 'mean'
values_vv = (image_collection
          .select(VV)
          .reduce(statistic)
          .sample(
              region=geometry,
              scale=scale,
              projection=crs,
              geometries=True,
              dropNulls=False,
          )
          .getInfo()
)
# values_vh = (image_collection
#           .select(VH)
#           .getRegion(geometry, scale=scale, crs=crs)
#           .getInfo()
# )
