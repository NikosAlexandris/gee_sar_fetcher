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
        statistic,
    ):
    """Tries to retrieving the number of pixels per image. If the total number
    of pixels exceeds the (currently) 5000 values, it slices the requested
    region in subregions and returns a nested list of sub-bounding box
    coordinates.
    """
    list_of_coordinates = list_coordinates(top_left, bottom_right, coordinates)
    try:
        polygon = ee.Geometry.Polygon(list_of_coordinates)
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
            list_of_coordinates = tile_coordinates(
                    total_count_of_pixels=composite_pixels_count,
                    coordinates=(top_left, bottom_right),
                    max_gee=maximum_gee_elements,
            )
        else:
            list_of_coordinates = tile_coordinates(
                    total_count_of_pixels=composite_pixels_count,
                    coordinates=coordinates,
                    max_gee=maximum_gee_elements,
            )
    print(f'Region sliced in '
          f'{len(list_of_coordinates)} subregions.'
    )
    return list_of_coordinates
