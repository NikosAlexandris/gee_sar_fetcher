from .utils import make_polygon
import numpy


def list_coordinates(top_left, bottom_right, coordinates=None):
    if (top_left is not None):
        list_of_coordinates = [make_polygon(top_left, bottom_right)]
    else:
        list_of_coordinates = [coordinates]
    return list_of_coordinates


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
    """Build a custom dictionary 'coordinates_dictionary' populated with values from
    the 'dictified_values' dictionnary

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
        lat = entry["latitude"]
        lon = entry["longitude"]
        new_key = str(lat)+":"+str(lon)

        if new_key in coordinates_dictionary:
            # Retrieving measured value
            coordinates_dictionary[new_key]["VV"].append(entry["VV"])
            coordinates_dictionary[new_key]["VH"].append(entry["VH"])
            tmstp = entry["time"]
            coordinates_dictionary[new_key]["timestamps"].append(tmstp//1000)

        else:
            coordinates_dictionary[new_key] = {}
            # Retrieving measured value
            coordinates_dictionary[new_key]["lat"] = lat
            coordinates_dictionary[new_key]["lon"] = lon
            coordinates_dictionary[new_key]["VV"] = [entry["VV"]]
            coordinates_dictionary[new_key]["VH"] = [entry["VH"]]
            tmstp = entry["time"]
            coordinates_dictionary[new_key]["timestamps"] = [tmstp//1000]

    return coordinates_dictionary


def composite_coordinates_dictionary(dictified_values):
    """
    The dictionnary coordinates_dictionary' will be populated (or updated) with
    values from the 'dictified_values' dictionnary

    Parameters
    ----------
    dictified_values :
        A dictionary of Sentinel-1 values

    coordinates_dictionary :
        A dictionnary matching to each coordinate key its values through time
        as well as its timestamps.

    Returns
    -------
    coordinates_dictionary
    """
    coordinates_dictionary = {}
    for entry in dictified_values:
        lat = entry["latitude"]
        lon = entry["longitude"]
        new_key = str(lat)+":"+str(lon)

        if new_key in coordinates_dictionary:
            # Retrieving measured value
            coordinates_dictionary[new_key]["VV"].append(entry["VV"])
            coordinates_dictionary[new_key]["VH"].append(entry["VH"])

        else:
            coordinates_dictionary[new_key] = {}
            # Retrieving measured value
            coordinates_dictionary[new_key]["lat"] = lat
            coordinates_dictionary[new_key]["lon"] = lon
            coordinates_dictionary[new_key]["VV"] = [entry["VV"]]
            coordinates_dictionary[new_key]["VH"] = [entry["VH"]]

    return coordinates_dictionary


def compare_coordinates_dictionaries(a, b):
    '''
    Given two coordinates dictionaries a and b, compare which one is closer to
    the North-Eastern direction

    Parameters
    ----------
    a : dict
        dict with keys ``"lon"`` and ``"lat"``
    b : dict
        dict with keys ``"lon"`` and ``"lat"``

    Returns
    -------
    int
        **-1** if ``a > b``, **1** if ``a < b``, **0** if ``a == b``
    '''
    if a["lat"] != b["lat"]:
        return 1 if a["lat"] < b["lat"] else -1
    elif a["lon"] != b["lon"]:
        return 1 if a["lon"] < b["lon"] else -1
    else:
        return 0


def generate_coordinates(
        height,
        width,
        pixel_values,
        unique_latitudes,
        unique_longitudes,
    ):
    """
    """
    coordinates = [
                    [latitude, longitude]
                    for longitude in unique_longitudes
                    for latitude in unique_latitudes
    ]
    coordinates = numpy.array(coordinates).reshape(height, width, 2)
    return coordinates
