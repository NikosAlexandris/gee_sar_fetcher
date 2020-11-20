from .constants import VV, VH, IW, ASCENDING
from .filter import filter_sentinel1_data
from tqdm import tqdm
import ee
from .compose import compose_sentinel1_data
from .dictify import dictify_pixel_values


__all__ = ["fetch_sentinel1_data"]

def fetch_sentinel1_data(
        start_date,
        end_date,
        geometry,
        scale,
        crs,
        pass_direction=ASCENDING,
    ):
    '''
    Retrieves and queries ImageCollection using input parameters and return
    data as a tuple of header and values.

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
    val_vv = (filtered_sentinel1_data
              .select(VV)
              .getRegion(geometry, scale=scale, crs=crs)
              .getInfo()
    )
    val_vh = (filtered_sentinel1_data
              .select(VH)
              .getRegion(geometry, scale=scale, crs=crs)
              .getInfo()
    )
    val_header = val_vv[0][1:] + [VH]
    val = [
            val_vv[i][1:]
            + [val_vh[i][val_vh[0].index(VH)]]
            for i in range(1, len(val_vv))
    ]
    return (val_header, val)


def fetch_composite_pixels(
        list_of_coordinates,
        start_date,
        end_date,
        scale,
        crs,
        pass_direction,
        statistic,
    ):
    header = []
    composite_values = []
    for coordinates in tqdm(list_of_coordinates):
        try:
            subregion = ee.Geometry.Polygon(
                    coords=[coordinates],
                    proj=crs,
                    geodesic=False,
            )
            subregion_header, subregion_values = compose_sentinel1_data(
                start_date=start_date,
                end_date=end_date,
                geometry=subregion,
                scale=scale,
                crs=crs,
                pass_direction=pass_direction,
                statistic=statistic,
            )
            composite_values.extend(subregion_values)
            if not header:
                header.extend(subregion_header)
        except Exception as e:
            print("Some exception occured:", e)
            pass

    pixel_values = dictify_pixel_values(
            header=header,
            pixel_values_list=composite_values,
    )
    return pixel_values
