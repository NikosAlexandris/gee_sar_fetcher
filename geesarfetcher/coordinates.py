def populate_coordinates_dictionary(dictified_values):
def list_coordinates(top_left, bottom_right, coordinates=None):
    if (top_left is not None):
        list_of_coordinates = [make_polygon(top_left, bottom_right)]
    else:
        list_of_coordinates = [coordinates]
    return list_of_coordinates


def latitudes_and_longitudes(pixel_values):
    """Get latitude and longitude values from a (retrieved) dictionary of
    'pixel_values'
    """
    latitudes, longitudes = tuple(
            zip(*[(pixel_value['lat'], pixel_value['lon'])
                for pixel_value in pixel_values])
    )
    unique_latitudes = numpy.unique(latitudes)
    unique_latitudes = unique_latitudes[::-1]
    unique_longitudes = numpy.unique(longitudes)
    return unique_latitudes, unique_longitudes



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
