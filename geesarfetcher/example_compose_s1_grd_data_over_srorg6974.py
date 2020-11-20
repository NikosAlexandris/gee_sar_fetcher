# imports
import os
import ee
ee.Initialize()
import datetime
from geesarfetcher.api import compose
import numpy
from numpy import savetxt

# constants
SENTINEL1_COLLECTION_ID = 'COPERNICUS/S1_GRD'
VV = 'VV'
VH = 'VH'
IW = 'IW'
ASCENDING = 'ASCENDING'
DESCENDING = 'DESCENDING'
SRORG6974 = 'SR-ORG:6974'  # projection

# where?
scale=1000
# top_left = [-104.77431630331856, 41.829889598264826]
# bottom_right = [-104.65140675742012, 41.81515375846025]
# top_left = [5.26948161, 49.97440374]
top_left = [7.26948161, 49.97440374]
bottom_right = [8.07913236, 48.90621773]
x_min = top_left[0]
y_min = bottom_right[1]
x_max = bottom_right[0]
y_max = top_left[1]
extent = (x_min, y_min, x_max, y_max)
geometry = ee.Geometry.Rectangle(extent, SRORG6974, False)

# when?
start_date = datetime.datetime(2019, 6, 1)
end_date = datetime.datetime(2019, 6, 30)

# compose
statistic = 'mean'
sentinel_1_composite = compose(
    top_left=top_left,
    bottom_right=bottom_right,
    start_date=start_date,
    end_date=end_date,
    ascending=True,
    scale=scale,
    crs=SRORG6974,
    statistic=statistic,
    n_jobs=30,
)

# write out
header = (',').join(['Latitude,Longitude,VV,VH'])
output = numpy.dstack((
    sentinel_1_composite['coordinates'],
    sentinel_1_composite['stack']
    )
)
filename = os.path.basename(__file__)
savetxt(
        fname=f'{filename}.csv',
        X=output[0],
        fmt='%.18f',
        delimiter=',',
        header=header,
        comments=''
)
