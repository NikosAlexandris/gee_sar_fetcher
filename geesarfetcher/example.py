from devtools import debug
# imports
import os
import ee
ee.Initialize()
import datetime
from geesarfetcher.sinusoidal import degrees_to_sinusoidal
from geesarfetcher.api import compose
from geesarfetcher.filter import filter_sentinel1_data

# constants
SENTINEL1_COLLECTION_ID = 'COPERNICUS/S1_GRD'
VV = 'VV'
VH = 'VH'
IW = 'IW'
ASCENDING = 'ASCENDING'
DESCENDING = 'DESCENDING'
SRORG6974 = 'SR-ORG:6974'  # projection

# where?
nsres=926.76896281
nw_long=5.27500244
nw_lat=49.98607421
se_long=8.07847752
se_lat=47.90267285
top_left = [nw_long, nw_lat]
bottom_right = [se_long, se_lat]
#
left, top, right, bottom = degrees_to_sinusoidal(
        west = nw_long,
        north = nw_lat,
        east = se_long,
        south = se_lat,
)
#-
extent = (left, bottom, right, top)
# geometry = ee.Geometry.Rectangle(
geometry = ee.Geometry.Polygon(
        coords=extent,
        proj=SRORG6974,
        geodesic=False
)
#-

# when?
start_date = datetime.datetime(2019, 6, 1)
end_date = datetime.datetime(2019, 6, 30)

# filter collection
filtered_sentinel1_data = filter_sentinel1_data(
        start_date=start_date,
        end_date=end_date,
        geometry=geometry,
        pass_direction=ASCENDING
)

# aggregate and count pixels
statistic = 'mean'
vv_pixel_count = (filtered_sentinel1_data
        .select(VV)
        .reduce(statistic)
        .sample(
            region=geometry,
            scale=nsres,
            projection=SRORG6974,
            dropNulls=False,
        )
        .size()
        .getInfo()
)
debug(locals())
