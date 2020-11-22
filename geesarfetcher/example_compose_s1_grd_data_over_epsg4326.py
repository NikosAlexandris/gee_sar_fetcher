import ee
ee.Initialize()
import datetime
from geesarfetcher.api import compose
import numpy
import os
from numpy import savetxt

sentinel_1_composite = compose(
    top_left=[7.26948161, 49.97440374],
    bottom_right=[8.07913236, 48.90621773],
    start_date=datetime.datetime(2019, 6, 1),
    end_date=datetime.datetime(2019, 6, 30),
    ascending=True,
    scale=1000,
    statistic='mean',
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
