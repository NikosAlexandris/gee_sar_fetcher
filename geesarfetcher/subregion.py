from devtools import debug
from .coordinates import list_coordinates
import ee
from .compose import count_composite_pixels
from .compose import compose_sentinel1_data
from .messages import MESSAGE_NO_BANDS_IN_COLLECTION
from .messages import VALUE_ERROR_NO_BANDS_IN_COLLECTION
from .utils import retrieve_max_pixel_count_from_composite
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
    """
    """
    list_of_coordinates = list_coordinates(top_left, bottom_right, coordinates)
    # retrieving the number of pixels per image
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
        # If the area is found to be too big
        if (str(e) == MESSAGE_NO_BANDS_IN_COLLECTION):
            raise ValueError(VALUE_ERROR_NO_BANDS_IN_COLLECTION)
        total_count_of_pixels = retrieve_max_pixel_count_from_composite(str(e))
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
                    (top_left, bottom_right)
            )
        else:
            list_of_coordinates = tile_coordinates(
                    total_count_of_pixels=composite_pixels_count,
                    coordinates
            )

    ## RETRIEVE COORDINATES VALUES

    print(f'Region sliced in '
          f'{len(list_of_coordinates)} subregions.'
    )
    return list_of_coordinates


def populate_composite_subregion(
        start_date,
        end_date,
        subregion,
        scale,
        crs,
        pass_direction,
        statistic,
    ):
    """
    """
    header, values = compose_sentinel1_data(
            start_date=start_date,
            end_date=end_date,
            geometry=subregion,
            scale=scale,
            crs=crs,
            pass_direction=pass_direction,
            statistic=statistic,
    )
    return (header, values)
