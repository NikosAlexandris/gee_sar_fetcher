from helpers import define_interval
import datetime

# where?
SRORG6974 = 'SR-ORG:6974'  # projection
ewres=926.625433055833355
nsres=926.625433055000258
north=5556366.58391489
south=5327454.6501018
east=602106.99615688
west=377344.171763875
where='_'.join([
    str(west),
    str(north),
    str(east),
    str(south)
])
top_left = [west, north]
bottom_right = [east, south]
locations = [ (top_left, bottom_right) ]

# when?
    # Around Landsat8 acquisitions on June 2019
    # 1. 20190613
    # 2. 20190629
date_1 = datetime.datetime(2019, 6, 13)
week_1 = define_interval(date_1, 3, 4)
date_2 = datetime.datetime(2019, 6, 29)
week_2 = define_interval(date_2, 3, 4)
intervals = [week_1, week_2]

# what?
image_collection = 'S1_GRD'
statistics = ['min', 'mean', 'median', 'max', 'count']
