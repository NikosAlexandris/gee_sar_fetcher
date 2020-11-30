import datetime
from datetime import timedelta
import numpy

DATA_TYPES = numpy.dtype([('x', numpy.float32), ('y', numpy.float32),('VV', numpy.float32), ('VH', numpy.float32)])
DATA_TYPES_EXTENDED = [('Start', (numpy.str_, 8)), ('End', (numpy.str_, 8))]
DELIMITER = ','
FIELD_FORMAT = '%.7f'
FIELD_FORMATS = ['%f', '%f', '%f', '%f', '%s', '%s']
CSV_HEADER = (',').join(['Northing,Easting,VV,VH'])
CSV_HEADER_EXTENDED = (',').join([CSV_HEADER, 'Start,End'])


def define_interval(
        start_date,
        days_pre,
        days_post,
    ):
    """Defines a time interval in form of a tuple

    Parameters
    ----------
    start_date : datetime.datetime
        A datetime object

    days_pre : int
        An integer indicating how many days before the origin_date

    days_post : int
        An integer indicating how many days after the origin_date. GEE's end
        data for filtering dates is exclusive, meaning the last date indicated
        in `end` is not considered.

    Returns
    -------
    interval : tuple
        A tuple of datetime.datetime objects indicating the start and the end
        of an interval
    """
    origin_date = datetime.datetime(2019, 6, 13)
    start = origin_date - timedelta(days=3)
    end = origin_date + timedelta(days=4)
    return (start, end)


def structure_array(array, data_types, start_date, end_date):
    """
    # convert to structured array
    """
    structured_array = numpy.array(
            numpy.rec.fromarrays(
                array.transpose(),
                names=data_types.names)
            .astype(dtype=data_types)
            .tolist(),
            dtype=data_types
    )
    # define final structure
    final_data_types = numpy.dtype(structured_array.dtype.descr + DATA_TYPES_EXTENDED)
    final_structured_array = numpy.zeros(
            structured_array.shape,
            dtype=final_data_types,
    )
    # copy over the existing data
    for field in structured_array.dtype.names:
        final_structured_array[field] = structured_array[field]

    # fill-in start and end dates
    final_structured_array['Start'] = start_date
    final_structured_array['End'] = end_date

    return final_structured_array


def build_output_filename(
        image_collection,
        location,
        interval,
        statistic,
    ):
    """
    """
    where='_'.join([
            str(location[0][0]),
            str(location[0][1]),
            str(location[1][0]),
            str(location[1][1]),
    ])
    start_date=interval[0].strftime("%Y%m%d")
    end_date=interval[1].strftime("%Y%m%d")
    when='_'.join([
        start_date,
        end_date,
    ])
    filename = '_'.join([
            image_collection,
            where,
            when,
            statistic,
    ])
    return filename


def stack_composite_data(composite_data):
    """
    """
    coordinates = composite_data['coordinates']
    coordinates = coordinates.reshape(
            coordinates.shape[0]*coordinates.shape[1], coordinates.shape[-1]
    )
    stack = composite_data['stack']
    stack = stack.reshape(
            stack.shape[0]*stack.shape[1], stack.shape[-1]
    )
    return numpy.hstack((coordinates, stack))
