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
# from geesarfetcher.compose import compose_sentinel1_data
from geesarfetcher.compose import compose

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

# compose
statistic = 'mean'
# sentinel_1_composite = compose_sentinel1_data(
#     start_date=start_date,
#     end_date=end_date,
#     geometry=geometry,
#     scale=scale,
#     crs=crs,
#     pass_direction=pass_direction,
#     polarisation=VV,
#     statistic=statistic,
# )
sentinel_1_composite = compose(
    top_left=top_left,
    bottom_right=bottom_right,
    start_date=start_date,
    end_date=end_date,
    ascending=False,
    scale=scale,
    crs=crs,
    statistic=statistic,
)

