from devtools import debug
# LIBRARY IMPORTS
import ee
import warnings
from datetime import datetime, date, timedelta
from tqdm import tqdm
# from pqdm.processes import pqdm
from functools import cmp_to_key
import numpy as np
from joblib import Parallel, delayed
import os

# LOCAL IMPORTS
from .constants import ASCENDING, DESCENDING
from .constants import VV, VH
from .constants import MEAN
from .messages import MESSAGE_NO_BANDS_IN_COLLECTION
from .messages import VALUE_ERROR_NO_BANDS_IN_COLLECTION
from .messages import VALUE_ERROR_NO_COORDINATES
from .utils import make_polygon
from .utils import tile_coordinates
from .utils import define_image_shape
from .utils import retrieve_max_pixel_count_from_composite
from .utils import compare_coordinates_dictionaries
from .utils import get_date_interval_array
from .fetcher import fetch_sentinel1_data
from .filter import filter_sentinel1_data
from .coordinates import composite_coordinates_dictionary

def compose_sentinel1_data(
        start_date,
        end_date,
        geometry,
        scale,
        crs,
        pass_direction=ASCENDING,
        statistic=MEAN,
    ):
    '''
    Composes an image from an ImageCollection using input parameters and return data as a tuple of header and values.

    Parameters
    ----------
    start_date : str
        str following the pattern ``'yyyy-mm-dd'`` describing the start date of
        the time interval

    end_date : str
        str following the pattern ``'yyyy-mm-dd'`` describing the end date of
        the time interval

    geometry : ee.Geometry
        Geometry object defining the area of process

    scale : int
        Scale parameters of the getRegion() function. Defaulting at ``20``,
        change it to change the scale of the final data points. The highest,
        the lower the spatial resolution. Should be at least ``10``.

    pass_direction : str, optional
        Defines the pass direction to set for the data retrieval process

    Returns
    -------
    (val_header, val) : tuple
        val_header corresponds to the ``list of str`` describing the fields of
        the val array. The val array is a ``list`` of data records, each
        represented as a ``list`` of the same size as the val_header array.
    '''
    filtered_sentinel1_data = filter_sentinel1_data(
            start_date=start_date,
            end_date=end_date,
            geometry=geometry,
            pass_direction=pass_direction
    )
    values_vv = (filtered_sentinel1_data
              .select(VV)
              .reduce(statistic)
              .sample(
                  region=geometry,
                  scale=scale,
                  projection=crs,
                  geometries=True,
                  dropNulls=False,
              )
              .getInfo()
    )
    values_vh = (filtered_sentinel1_data
              .select(VH)
              .reduce(statistic)
              .sample(
                  region=geometry,
                  scale=scale,
                  projection=crs,
                  geometries=True,
                  dropNulls=False,
              )
              .getInfo()
    )
    header = ([
                'longitude',
                'latitude',
                'start_date',
                'end_date',
                VV,
                VH]
    )
    vv = []
    for feature in values_vv['features']:
        coordinates = feature['geometry']['coordinates']
        feature_property = feature['properties']
        value_vv = feature_property.get(VV + '_' + statistic)
        vv.extend([coordinates + [value_vv]])
    vh = []
    for feature in values_vh['features']:
        coordinates = feature['geometry']['coordinates']
        feature_property = feature['properties']
        value_vh = feature_property.get(VH + '_' + statistic)
        vh.extend([coordinates + [value_vh]])
    values = [
              vv[idx][:2] +
              [start_date] +
              [end_date] +
              [vv[idx][2]] +
              [vh[idx][2]]
              for idx in range(len(vv))
    ]
    return (header, values)

def compose(
    top_left=None,
    bottom_right=None,
    coordinates=None,
    start_date: datetime = date.today()-timedelta(days=365),
    end_date: datetime = date.today(),
    ascending: bool = True,
    scale: int = 10,
    crs: str = 'EPSG:4326',
    statistic: str = 'mean',
    n_jobs: int = 1,
):
    '''Fetches a composite of SAR data in the form of a dictionnary with image data as well as timestamps

    Parameters
    ----------
    top_left : tuple of float, optional
        Top left coordinates (lon, lat) of the Region

    bottom_right : tuple of float, optional
        Bottom right coordinates (lon, lat) of the Region

    coordinates : tuple of tuple of float or list of list of float, optional
        If `top_left` and `bottom_right` are not specified, we expect `coordinates`
        to be a list (resp. tuple) of the form ``[top_left, bottom_right]``
        (resp. ``(top_left, bottom_right)``)

    start_date : datetime.datetime, optional
        First date of the time interval

    end_date : datetime.datetime, optional
        Last date of the time interval

    ascending : boolean, optional
        The trajectory to use when selecting data

    scale : int, optional
        Scale parameters of the getRegion() function. Defaulting at ``20``,
        change it to change the scale of the final data points. The highest,
        the lower the spatial resolution. Should be at least ``10``.

    statistic : str
        The descriptive statistic as per Google Earth Engine's reducers.
    n_jobs : int, optional
        Set the parallelisation factor (number of threads) for the GEE data
        access process. Set to 1 if no parallelisation required.

    Returns
    -------
    `dict`
        Dictionnary with two keys:

            ``"stacks"``
                4-D array containing db intensity measure (`numpy.ndarray`),
                ``(height, width, time_series_length, pol_count)``

            ``"coordinates"``
                3-D array containg coordinates where ``[:,:,0]`` provides
                access to latitude and ``[:,:,1]`` provides access to
                longitude, (`numpy.ndarray`), ``(height, width, 2)``

            ``"timestamps"``
                list of acquisition timestamps of size (time_series_length,)
                (`list of str`)

            ``"metadata"``
                Dictionnary describing data for each axis of the stack and the
                coordinates
    '''
    # date_intervals = get_date_interval_array(start_date, end_date)
    pass_direction = ASCENDING if ascending else DESCENDING

    if (top_left is not None):
        list_of_coordinates = [make_polygon(top_left, bottom_right)]
    else:
        list_of_coordinates = [coordinates]

    # retrieving the number of pixels per image
    try:
        polygon = ee.Geometry.Polygon(list_of_coordinates)
        sentinel_1_roi = compose_sentinel1_data(
            start_date=start_date,
            end_date=end_date,
            geometry=polygon,
            scale=scale,
            crs=crs,
            pass_direction=pass_direction,
            statistic=statistic,
        )
    except Exception as e:
        # If the area is found to be too big
        if (str(e) == MESSAGE_NO_BANDS_IN_COLLECTION):
            raise ValueError(VALUE_ERROR_NO_BANDS_IN_COLLECTION)
        total_count_of_pixels = retrieve_max_pixel_count_from_composite(str(e))
        if top_left is not None:
            list_of_coordinates = tile_coordinates(
                    total_count_of_pixels,
                    (top_left, bottom_right)
            )
        else:
            list_of_coordinates = tile_coordinates(
                    total_count_of_pixels,
                    coordinates
            )

    ###################################
    ## RETRIEVING COORDINATES VALUES ##
    ## FOR EACH DATE INTERVAL        ##
    ###################################
    print(f'Region sliced in '
           '{len(list_of_coordinates)} subregions.'
    )
    def populate_composite_subregion(
            start_date,
            end_date,
            subregion,
            scale,
            crs,
            pass_direction,
            statistic,
    ):
        try:
            val_header, val = compose_sentinel1_data(
                start_date=start_date,
                end_date=end_date,
                geometry=subregion,
                scale=scale,
                crs=crs,
                pass_direction=pass_direction,
                statistic=statistic,
            )
            vals.extend(val)
            if len(headers) == 0:
                headers.extend(val_header)
        except Exception as e:
            pass

    for coordinates in tqdm(list_of_coordinates):
        vals = []
        headers = []
        subregion = ee.Geometry.Polygon([coordinates])
        # Fill vals with values.
        populate_composite_subregion(start_date, end_date, subregion, scale, crs, pass_direction, statistic)
        # number_of_cpu = joblib.cpu_count()
        # delayed_functions = [delayed(populate_composite_subregion)(start_date, end_date, subregion, scale, crs, pass_direction, statistic)
        #     for subregion (subregion := _gee_geometry_polygon(coordinates) for coordinates in tqdm(list_of_coordinates)]
        # parallel_pool = Parallel(n_jobs=number_of_cpu, require='sharedmem')
        # parallel_pool(delayed_functions)


    latitudes, longitudes = tuple(
                                    zip(*[(p["lat"], p["lon"])
                                    for p in pixel_values])
                            )
    unique_latitudes = np.unique(latitudes)
    unique_latitudes = unique_latitudes[::-1]
    latitudes_dictionary = {
            unique_latitudes[i]: i
            for i in range(len(unique_latitudes))
    }
    unique_longitudes = np.unique(longitudes)
    longitudes_dictionary = {
            unique_longitudes[i]: i
            for i in range(len(unique_longitudes))
    }
    coordinates = [
                    [latitude, longitude]
                    for longitude in unique_longitudes
                    for latitude in unique_latitudes
                ]
    width, height = len(unique_longitudes), len(unique_latitudes)
    coordinates = np.array(coordinates).reshape(height, width, 2)
