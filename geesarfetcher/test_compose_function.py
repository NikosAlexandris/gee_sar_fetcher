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
from geesarfetcher.filter import filter_sentinel1_data
# from geesarfetcher.compose import compose_sentinel1_data
from geesarfetcher.compose import compose

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

# # step-by-step
# filtered_sentinel1_data = filter_sentinel1_data(
#         start_date=start_date,
#         end_date=end_date,
#         geometry=geometry,
#         pass_direction=pass_direction
# )
# values_vv = (filtered_sentinel1_data
#           .select(VV)
#           .reduce(statistic)
#           .sample(
#               region=geometry,
#               scale=scale,
#               projection=crs,
#               geometries=True,
#               dropNulls=False,
#           )
#           .getInfo()
# )
# values_vh = (filtered_sentinel1_data
#           .select(VH)
#           .reduce(statistic)
#           .sample(
#               region=geometry,
#               scale=scale,
#               projection=crs,
#               geometries=True,
#               dropNulls=False,
#           )
#           .getInfo()
# )
# header = ([
#             'longitude',
#             'latitude',
#             'start_date',
#             'end_date',
#             VV,
#             VH]
# )
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

# compose()
sentinel_1_composite = compose(
    top_left=top_left,
    bottom_right=bottom_right,
    start_date=start_date,
    end_date=end_date,
    ascending=True,
    scale=scale,
    crs=crs,
    statistic=statistic,
)

