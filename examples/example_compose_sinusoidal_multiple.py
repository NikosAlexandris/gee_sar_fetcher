import ee
ee.Initialize()
from where_when_what import SRORG6974
from where_when_what import nsres
from where_when_what import locations
from where_when_what import intervals
from where_when_what import image_collection
from where_when_what import statistics
from geesarfetcher.api import compose
from geesarfetcher.api import write_to_csv

print(
        'Input parameters\n'
        f' Image collection: {image_collection}\n'
        f' Location:         {locations}\n'
        f' Projection:       {SRORG6974}\n'
        f' Resolution:       {nsres}\n'
        f' Intervals:        {intervals}\n'
        f' Statistics:       {statistics}\n'
)

print(f'Composing Sentinel-1 SAR data over')
# for dataset in DATASETS:
for location in locations:
    print(f'  Location: {location}')
    top_left = location[0]
    bottom_right = location[1]

    for ascending in [True, False]:
        print(f'  Ascending pass direction: {ascending}')

        for interval in intervals:
            print(f'  Interval: {interval}')
            start_date = interval[0]
            end_date = interval[1]

            for statistic in statistics:
                print(f'  Statistic: {statistic}')
                composite = compose(
                        top_left=top_left,
                        bottom_right=bottom_right,
                        start_date=start_date,
                        end_date=end_date,
                        ascending=ascending,
                        scale=nsres,
                        crs=SRORG6974,
                        statistic=statistic,
                        n_jobs=30,
                )
                write_to_csv(
                        composite_data=composite,
                        image_collection=image_collection,
                        location=location,
                        ascending=ascending,
                        interval=interval,
                        statistic=statistic,
                        structured=True,
                )
                print('\n')
