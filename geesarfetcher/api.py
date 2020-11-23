import ee
import warnings
from datetime import datetime, date, timedelta

from .constants import ASCENDING, DESCENDING
from .constants import VV, VH
from .constants import MEAN
from .messages import VALUE_ERROR_NO_COORDINATES
from .assertions import assert_inputs
from .subregion import slice_region
from .fetcher import fetch_composite_pixels
from .coordinates import northings_and_eastings
from .coordinates import generate_coordinates
from .image import generate_image
from .data_structure import strucure_data

def fetch():
    """This function performs the following steps:
        - assert inputs
        - get date intervals
        - set pass direction
        - tile bounding box coordinates
        - fetch data for tiles and date intervals
        - get timestamps
        - get northings, eastings
        - get image height, width
        - get coordinates
        - get image data structure
        - return data structure
    """
    # assert inputs
    assert_inputs(
            coordinates=coordinates,
            top_left=top_left,
            bottom_right=bottom_right,
            start_date=start_date,
            end_date=end_date,
    )

    # get date intervals
    date_intervals = get_date_interval_array(start_date, end_date)

    # set pass direction
    pass_direction = ASCENDING if ascending else DESCENDING

    # tile bounding box coordinates
    list_of_coordinates = slice_region(
        top_left=top_left,
        bottom_right=bottom_right,
        coordinates=coordinates,
        start_date=start_date,
        end_date=end_date,
        scale=scale,
        crs=crs,
        pass_direction=pass_direction,
    )

    # fetch data for tiles and date intervals
    # ------------------------------------------------------------- REFACTOR ---

    # get northings, eastings
    northings, eastings = northings_and_eastings(composite_pixel_values)

    # get image data structure
    image = generate_image(
            pixel_values=composite_pixel_values,
            unique_northings=northings,
            unique_eastings=eastings,
    )
    # get coordinates
    coordinates = generate_coordinates(
            pixel_values=composite_pixel_values,
            unique_northings=northings,
            unique_eastings=eastings,
    )
    # get timestamps
    timestamps = np.unique(
            [
                datetime.fromtimestamp(pixel_values[i]['timestamps'][j]).date()
                for i in range(len(pixel_values))
                for j in range(len(pixel_values[i]['timestamps']))
            ]
    )
    # return data structure
    return strucure_data(image, coordinates, timestamps)


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
    '''Fetches a composite of SAR data in the form of a dictionnary with image
    data as well as timestamps.

        The function performs the following steps:

        - assert inputs
        - set pass direction
        - tile bounding box coordinates
        - fetch data for tiles
        - get timestamps
        - get northings, eastings
        - get image height, width
        - get coordinates
        - get image data structure
        - return data structure

    Parameters
    ----------
    top_left : tuple of float, optional
        Top left coordinates (lon, lat) of the Region

    bottom_right : tuple of float, optional
        Bottom right coordinates (lon, lat) of the Region

    coordinates : tuple of tuple of float or list of list of float, optional
        If `top_left` and `bottom_right` are not specified, we expect
        `coordinates` to be a list (resp. tuple) of the form ``[top_left,
        bottom_right]`` (resp. ``(top_left, bottom_right)``)

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
    assert_inputs(
            coordinates=coordinates,
            top_left=top_left,
            bottom_right=bottom_right,
            start_date=start_date,
            end_date=end_date,
    )
    pass_direction = ASCENDING if ascending else DESCENDING
    list_of_coordinates = slice_composite_region(
        top_left=top_left,
        bottom_right=bottom_right,
        coordinates=coordinates,
        start_date=start_date,
        end_date=end_date,
        scale=scale,
        crs=crs,
        pass_direction=pass_direction,
        statistic=statistic,
    )
    composite_pixel_values = fetch_composite_pixels(
        list_of_coordinates=list_of_coordinates,
        start_date=start_date,
        end_date=end_date,
        scale=scale,
        crs=crs,
        pass_direction=pass_direction,
        statistic=statistic,
    )
    northings, eastings = northings_and_eastings(c
            omposite_pixel_values
    )
    image = generate_composite_image(
            pixel_values=composite_pixel_values,
            unique_northings=northings,
            unique_eastings=eastings,
    )
    coordinates = generate_coordinates(
            pixel_values=composite_pixel_values,
            unique_northings=northings,
            unique_eastings=eastings,
    )
    timestamps = [start_date, end_date]
    return strucure_composite_data(image, coordinates, timestamps)

