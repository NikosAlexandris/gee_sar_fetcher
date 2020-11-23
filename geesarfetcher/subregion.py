from devtools import debug
from .coordinates import list_coordinates
import ee
from .compose import count_composite_pixels
from .compose import compose_sentinel1_data
from .messages import MESSAGE_NO_BANDS_IN_COLLECTION
from .messages import VALUE_ERROR_NO_BANDS_IN_COLLECTION
from .utils import read_max_elements_limit_from_error
from .utils import tile_coordinates


def slice_region(
        top_left,
        bottom_right,
        coordinates,
        start_date,
        end_date,
        scale,
        crs,
        pass_direction,
    ):
    """Slices the requested region in subregions and returns a nested list of
    sub-bounding box coordinates _if_ the total number of pixels inside the
    requested region exceeds the maximum returned (currently 5000) values, it
    slices

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

    scale : int, optional
        Scale parameters of the getRegion() function. Defaulting at ``20``,
        change it to change the scale of the final data points. The highest,
        the lower the spatial resolution. Should be at least ``10``.

    crs : str, optional
        Coordinate Reference System

    pass_direction : str, optional
        Defines the pass direction to set for the data retrieval process:
            ``"ascending"`` (default) or ``"descending"``

    statistic : str
        The descriptive statistic as per Google Earth Engine's reducers.

    Returns
    -------
    list_of_coordinates
    """
    list_of_coordinates = list_coordinates(top_left, bottom_right, coordinates)
    try:
        polygon = ee.Geometry.Polygon(
                coords=list_of_coordinates,
                proj=crs,
                geodesic=False,
        )
        sentinel_1_roi = fetch_sentinel1_data(
            start_date=date_intervals[0][0],
            end_date=date_intervals[-1][1],
            geometry=polygon,
            scale=scale,
            crs=crs,
            pass_direction=pass_direction,
        )
    except Exception as e:
        if (str(e) == MESSAGE_NO_BANDS_IN_COLLECTION):
            raise ValueError(VALUE_ERROR_NO_BANDS_IN_COLLECTION)
        maximum_gee_elements = read_max_elements_limit_from_error(str(e))
        composite_pixels_count = count_composite_pixels(
            start_date=start_date,
            end_date=end_date,
            geometry=polygon,
            scale=scale,
            crs=crs,
            pass_direction=pass_direction,
            statistic=statistic,
        )
        if top_left is not None:
            bounding_box_coordinates=(top_left, bottom_right),
        else:
            bounding_box_coordinates=coordinates,
        list_of_coordinates = tile_coordinates(
                total_count_of_pixels=composite_pixels_count,
                coordinates=bounding_box_coordinates,
                max_gee=maximum_gee_elements,
        )
    print(f'Region sliced in '
          f'{len(list_of_coordinates)} subregions.'
    )
    return list_of_coordinates

def slice_composite_region(
        top_left,
        bottom_right,
        coordinates,
        start_date,
        end_date,
        scale,
        crs,
        pass_direction,
        statistic,
    ):
    """Slices the requested region in subregions and returns a nested list of
    sub-bounding box coordinates _if_ the total number of pixels inside the
    requested region exceeds the maximum returned (currently 5000) values, it
    slices

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

    scale : int, optional
        Scale parameters of the getRegion() function. Defaulting at ``20``,
        change it to change the scale of the final data points. The highest,
        the lower the spatial resolution. Should be at least ``10``.

    crs : str, optional
        Coordinate Reference System

    pass_direction : str, optional
        Defines the pass direction to set for the data retrieval process:
            ``"ascending"`` (default) or ``"descending"``

    statistic : str
        The descriptive statistic as per Google Earth Engine's reducers.

    Returns
    -------
    list_of_coordinates
    """
    list_of_coordinates = list_coordinates(top_left, bottom_right, coordinates)
    try:
        polygon = ee.Geometry.Polygon(
                coords=list_of_coordinates,
                proj=crs,
                geodesic=False,
        )
        sentinel1_composite = compose_sentinel1_data(
            start_date=start_date,
            end_date=end_date,
            geometry=polygon,
            scale=scale,
            crs=crs,
            pass_direction=pass_direction,
            statistic=statistic,
        )
    except Exception as e:
        if (str(e) == MESSAGE_NO_BANDS_IN_COLLECTION):
            raise ValueError(VALUE_ERROR_NO_BANDS_IN_COLLECTION)
        maximum_gee_elements = read_max_elements_limit_from_error(str(e))
        composite_pixels_count = count_composite_pixels(
            start_date=start_date,
            end_date=end_date,
            geometry=polygon,
            scale=scale,
            crs=crs,
            pass_direction=pass_direction,
            statistic=statistic,
        )
        if top_left is not None:
            bounding_box_coordinates=(top_left, bottom_right),
        else:
            bounding_box_coordinates=coordinates,
        list_of_coordinates = tile_coordinates(
                total_count_of_pixels=composite_pixels_count,
                coordinates=bounding_box_coordinates,
                max_gee=maximum_gee_elements,
        )
    print(f'Region sliced in '
          f'{len(list_of_coordinates)} subregions.'
    )
    return list_of_coordinates
