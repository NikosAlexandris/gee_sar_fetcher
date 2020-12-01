import ee
ee.Initialize()
import datetime
from geesarfetcher.api import compose
from geesarfetcher.api import write_to_csv
from where_when_what import image_collection

n=49.9695488705556
s=47.9108967116667
w=5.25413596111111
e=8.07845648166667

top_left = [w, n]
bottom_right = [e, s]
location = (top_left, bottom_right)

start_date = datetime.datetime(2019, 6, 1)
end_date = datetime.datetime(2019, 6, 6)
interval = (start_date, end_date)

#
statistic = 'mean'
composite = compose(
    top_left=top_left,
    bottom_right=bottom_right,
    start_date=start_date,
    end_date=end_date,
    ascending=True,
    scale=1000,
    statistic=statistic,
    n_jobs=30,
)

# write out
write_to_csv(
        composite_data=composite,
        image_collection=image_collection,
        location=location,
        interval=interval,
        statistic=statistic,
        structured=False,
)
