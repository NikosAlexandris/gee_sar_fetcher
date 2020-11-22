from .constants import VV
from .constants import VH
from .utils import make_polygon
import numpy


def list_coordinates(top_left, bottom_right, coordinates=None):
    if (top_left is not None):
        list_of_coordinates = [make_polygon(top_left, bottom_right)]
    else:
        list_of_coordinates = [coordinates]
    return list_of_coordinates


def northing_and_easting(dictionary):
    """
    Retrieve and return the northing and easting strings to be used as
    dictionary keys

    Parameters
    ----------
    dictionary : dict

    Returns
    -------
    northing, easting : tuple

    """
    if not 'x' and 'y' in dictionary.keys():
        northing = 'latitude'
        easting = 'longitude'
    else:
        northing = 'x'
        easting = 'y'
    return northing, easting


def northings_and_eastings(pixel_values):
    """Get northing and easting values from a (retrieved) dictionary of
    'pixel_values'
    """
    northings = []
    eastings = []
    for entry in pixel_values:
        northing, easting = northing_and_easting(entry)
        northings.append(entry[northing])
        eastings.append(entry[easting])
    unique_northings = numpy.unique(northings)
    unique_northings = unique_northings[::-1]  # why?
    unique_eastings = numpy.unique(eastings)
    return unique_northings, unique_eastings


def populate_coordinates_dictionary(dictified_values):
    """Build a custom dictionary 'coordinates_dictionary' populated with values
    from the 'dictified_values' dictionnary

    Parameters
    ----------
    dictified_values :
        A dictionary of Sentinel-1 values

    Returns
    -------
    coordinates_dictionary :
        A dictionnary matching to each coordinate key its values through time
        as well as its timestamps.

    """
    coordinates_dictionary = {}
    for entry in dictified_values:
        lat = entry['latitude']
        lon = entry['longitude']
        new_key = str(lat)+':'+str(lon)

        if new_key in coordinates_dictionary:
            # Retrieving measured value
            coordinates_dictionary[new_key][VV].append(entry[VV])
            coordinates_dictionary[new_key][VH].append(entry[VH])
            tmstp = entry['time']
            coordinates_dictionary[new_key]['timestamps'].append(tmstp//1000)

        else:
            coordinates_dictionary[new_key] = {}
            # Retrieving measured value
            coordinates_dictionary[new_key]['lat'] = lat
            coordinates_dictionary[new_key]['lon'] = lon
            coordinates_dictionary[new_key][VV] = [entry[VV]]
            coordinates_dictionary[new_key][VH] = [entry[VH]]
            tmstp = entry['time']
            coordinates_dictionary[new_key]['timestamps'] = [tmstp//1000]

    return coordinates_dictionary


def composite_coordinates_dictionary(dictified_values):
    """A dictionnary will be populated (or updated) with values from the
    'dictified_values' dictionnary

    Parameters
    ----------
    dictified_values :
        A dictionary of Sentinel-1 values

    coordinates_dictionary :
        A dictionnary matching to each coordinate key its values

    Returns
    -------
    coordinates_dictionary
    """
    dictionary = {}
    for entry in dictified_values:
        northing, easting = northing_and_easting(entry)
        coordinates = str(entry.get(northing)) + ':' + str(entry.get(easting))
        if coordinates in dictionary:
            dictionary[coordinates][VV].append(entry[VV])
            dictionary[coordinates][VH].append(entry[VH])
        else:
            dictionary[coordinates] = {}
            dictionary[coordinates][northing] = entry.get(northing)
            dictionary[coordinates][easting] = entry.get(easting)
            dictionary[coordinates]['start_date'] = entry['start_date']
            dictionary[coordinates]['end_date'] = entry['end_date']
            dictionary[coordinates][VV] = [entry[VV]]
            dictionary[coordinates][VH] = [entry[VH]]
    return dictionary


def compare_coordinates_dictionaries(a, b):
    '''
    Given two coordinates dictionaries a and b, compare which one is closer to
    the North-Eastern direction

    Parameters
    ----------
    a : dict
        dict with keys ``"longitude"`` and ``"latitude"``
    b : dict
        dict with keys ``"longitude"`` and ``"latitude"``

    Returns
    -------
    int
        **-1** if ``a > b``, **1** if ``a < b``, **0** if ``a == b``
    '''
    if not 'x' and 'y' in a and not 'a' and 'y' in b:
        northing = 'latitude'
        easting = 'longitude'
    else:
        northing = 'x'
        easting = 'y'
    if a[northing] != b[northing]:
        return 1 if a[northing] < b[northing] else -1
    elif a[easting] != b[easting]:
        return 1 if a[easting] < b[easting] else -1
    else:
        return 0


def generate_coordinates(
        height,
        width,
        pixel_values,
        unique_northings,
        unique_eastings,
    ):
    """
    """
    coordinates = [
                    [northing, easting]
                    for easting in unique_eastings
                    for northing in unique_northings
    ]
    coordinates = numpy.array(coordinates).reshape(height, width, 2)
    return coordinates
