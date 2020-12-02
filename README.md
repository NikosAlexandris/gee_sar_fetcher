# GEE SAR Fetcher

An easy-to-use Python library to download SAR GRD imagery from Google Earth
Engine.

**Note**

> THIS IS AN **experimental fork** of the original pacakge `geesarfetcher`.
> The aim here is to provide an API to retrieve composite images (in common
> Remote Sensing terms: aggregate a time series) from the `S1_GRD` image
> collection.  For example, the mean of SAR acquisitions over a specific region
> and period of time.


## Introduction

Access Google's multi-petabytes of SAR Imagery data from your python code with
*no dimension restraint*. Simply supply coordinates, a time interval and obtain
a stack of Sentinel-1 preprocessed PolSAR images.  This enables quick data
analysis of GRD images to get better insights of the temporal dimension in SAR
data without having to bother with essential but potentially time-consuming
steps such as coregistration or calibration. 

Compatible with python 3.

## Usage

### Python Import

The main function of this library is the ``fetch`` function:
```python
from geesarfetcher import fetch
from datetime import date, timedelta

fetch(
    top_left = [-104.77431630331856, 41.81515375846025], 
    bottom_right = [-104.65140675742012, 41.729889598264826],
    start_date = date.today()-timedelta(days=15),
    end_date = date.today(),
    ascending=False,
    scale=10,
    n_jobs=1
) # returns a dictionnary with access to the data through the 'stack' keyword and to its timestamps through the 'timestamps' keyword
```

The ``compose`` function:
```python
from geesarfetcher.api import compose
import datetime

compose(
    top_left=[7.26948161, 49.97440374],
    bottom_right=[8.07913236, 48.90621773],
    start_date=datetime.datetime(2019, 6, 1),
    end_date=datetime.datetime(2019, 6, 30),
    ascending=True,
    scale=1000,
    statistic='mean',
    n_jobs=30,
)  # returns a dictionary with access to (meta-)data through the keywords 'stack', 'coordinates' and 'timestamps' 
```
or aggregating pixel values over another projection system (i.e. MODIS'
Sinusoidal grid) and using multiple CPUs (i.e. `n_jobs=30`):
```python
from geesarfetcher.api import compose
import datetime

composite = compose(
    top_left=top_left,
    bottom_right=bottom_right,
    start_date=datetime.datetime(2019, 6, 1),
    end_date=datetime.datetime(2019, 6, 30),
    ascending=True,
    scale=nsres,
    crs=SRORG6974,
    statistic=statistic,
    n_jobs=30,
)
```

## Installation

Access to Google Earth Engine is conditioned by the obtention of a [GEE
account](https://earthengine.google.com/).  Once created, you can install the
**geesarfetcher** API and register an identifying token for your Python working
environment using the following commands:
```
pip install geesarfetcher
earthengine authenticate
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.  Please make sure to update tests as
appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
