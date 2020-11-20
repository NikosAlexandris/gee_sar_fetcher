# imports
import os
import ee
ee.Initialize()
import datetime
from geesarfetcher.sinusoidal import degrees_to_sinusoidal
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
# g.region \
#        vect=region_modis_landsat8_ecostress@PERMANENT -p
# nsres=926.76896281 ewres=924.94989462 -pelag
# projection=99
# zone=0
# n=5539298.09071537
# s=5307605.85001287
# w=378304.50689958
# e=603992.28118686
nsres=926.76896281
# ewres=924.94989462
# rows=250
# cols=244
# cells=61000
nw_long=5.27500244
nw_lat=49.98607421
# ne_long=8.42194767
# ne_lat=49.98607421
se_long=8.07847752
se_lat=47.90267285
# sw_long=5.05987336
# sw_lat=47.90267285
# center_long=6.70481323
# center_lat=48.94446807
# ns_extent=231692.240703
# ew_extent=225687.774287

left, top, right, bottom = degrees_to_sinusoidal(
        west = nw_long,
        north = nw_lat,
        east = se_long,
        south = se_lat,
)
top_left = [left, top]
bottom_right = [right, bottom]
#-
#extent = (left, bottom, right, top)
#geometry = ee.Geometry.Rectangle(
#        coords=extent,
#        proj=SRORG6974,
#        geodesic=False
#)
##-

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
    scale=nsres,
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
