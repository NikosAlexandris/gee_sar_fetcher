from .constants import ASCENDING
from .constants import MEAN
from .constants import VV
from .constants import VH
from .filter import filter_sentinel1_data
import ee

def count_composite_pixels(
        start_date,
        end_date,
        geometry,
        scale,
        crs,
        pass_direction,
        statistic=MEAN,
        ):
    """
    """
    filtered_sentinel1_data = filter_sentinel1_data(
            start_date=start_date,
            end_date=end_date,
            geometry=geometry,
            pass_direction=pass_direction
    )
    vv_pixel_count = (filtered_sentinel1_data
            .select(VV)
            .reduce(statistic)
            .sample(
                region=geometry,
                scale=scale,
                projection=crs,
                dropNulls=False,
            )
            .size()
            .getInfo()
    )
    vh_pixel_count = (filtered_sentinel1_data
            .select(VV)
            .reduce(statistic)
            .sample(
                region=geometry,
                scale=scale,
                projection=crs,
                dropNulls=False,
            )
            .size()
            .getInfo()
    )
    return max(vv_pixel_count, vh_pixel_count)

def compose_sentinel1_data(
        start_date,
        end_date,
        geometry,
        scale,
        crs,
        pass_direction,
        statistic=MEAN,
    ):
    '''
    Composes an image from an ImageCollection using input parameters and return
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
    values_vv = (filtered_sentinel1_data
            .select(VV)
            .reduce(statistic)
            .addBands(ee.Image.pixelCoordinates(projection=crs))
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
            .addBands(ee.Image.pixelCoordinates(projection=crs))
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
                'x',
                'y',
                'start_date',
                'end_date',
                VV,
                VH
    ])
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
