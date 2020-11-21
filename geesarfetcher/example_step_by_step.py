from devtools import debug
import ee
ee.Initialize()
import datetime
from geesarfetcher.constants import ASCENDING
from geesarfetcher.constants import VV
from geesarfetcher.constants import VH
from geesarfetcher.sinusoidal import degrees_to_sinusoidal
from geesarfetcher.coordinates import list_coordinates
from geesarfetcher.filter import filter_sentinel1_data

# where?
SRORG6974 = 'SR-ORG:6974'
scale = nsres=926.76896281
nw_long = 7.9
nw_lat = 49.0
se_long = 8.0
se_lat = 48.9
left, top, right, bottom = degrees_to_sinusoidal(
        west = nw_long,
        north = nw_lat,
        east = se_long,
        south = se_lat,
)
top_left = [left, top]
bottom_right = [right, bottom]
coordinates=None
list_of_coordinates = list_coordinates(
        top_left,
        bottom_right,
        coordinates
)
polygon = ee.Geometry.Polygon(
        coords=list_of_coordinates,
        proj=SRORG6974,
        geodesic=False,
)

# when?
start_date = datetime.datetime(2019, 6, 1)
end_date = datetime.datetime(2019, 6, 30)
statistic = 'mean'

# get
filtered_sentinel1_data = filter_sentinel1_data(
        start_date=start_date,
        end_date=end_date,
        geometry=polygon,
        pass_direction=ASCENDING,
)
values_vv = (filtered_sentinel1_data
        .select(VV)
        .reduce(statistic)
        .addBands(ee.Image.pixelCoordinates(projection=SRORG6974))
        .sample(
            region=polygon,
            scale=scale,
            projection=SRORG6974,
            geometries=True,
            dropNulls=False,
        )
        .getInfo()
)
values_vh = (filtered_sentinel1_data
        .select(VH)
        .reduce(statistic)
        .addBands(ee.Image.pixelCoordinates(projection=SRORG6974))
        .sample(
            region=polygon,
            scale=scale,
            projection=SRORG6974,
            geometries=True,
            dropNulls=False,
        )
        .getInfo()
)
header = ([
            'longitude',
            'latitude',
            'x',
            'y',
            'start_date',
            'end_date',
            VV,
            VH
])
vv = []
for feature in values_vv['features']:
    feature_property = feature['properties']
    value_vv = [feature_property.get(VV + '_' + statistic)]
    coordinates_x = feature_property.get('x')
    coordinates_y = feature_property.get('y')
    coordinates_xy = [coordinates_x, coordinates_y]
    coordinates = feature['geometry']['coordinates']
    vv.extend([
        coordinates
        + coordinates_xy
        + value_vv
    ])
vh = []
for feature in values_vh['features']:
    feature_property = feature['properties']
    value_vh = [feature_property.get(VH + '_' + statistic)]
    coordinates_x = feature_property.get('x')
    coordinates_y = feature_property.get('y')
    coordinates_xy = [coordinates_x, coordinates_y]
    coordinates = feature['geometry']['coordinates']
    vh.extend([
        coordinates
        + coordinates_xy
        + value_vh
    ])
values = [
          vv[idx][:4] +
          [start_date] +
          [end_date] +
          [vv[idx][4]] +
          [vh[idx][4]]
          for idx in range(len(vv))
]
# debug(locals())

# Get Projection()
#
# If Projection != EPSG:4326:
#    Use 'x' and 'y'
# Else:
#     Use geographic coordinates
