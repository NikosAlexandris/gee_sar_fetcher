from .coordinates import composite_coordinates_dictionary
from .coordinates import compare_coordinates_dictionaries
from functools import cmp_to_key


def dictify_pixel_values(header, pixel_values_list):
    """

    Parameters
    ----------
    pixel_values :
        A list of lists of values returned from
        populate_composite_subregion()

    Returns
    -------
    """
    dictified_values = [
            dict(zip(header, values))
            for values in pixel_values_list
    ]
    per_coordinates_dictionary = composite_coordinates_dictionary(
            dictified_values=dictified_values,
    )
    pixel_values = [
            per_coordinates_dictionary[k]
            for k in per_coordinates_dictionary.keys()
    ]
    coordinates_dictionaries_comparison = cmp_to_key(compare_coordinates_dictionaries)
    pixel_values.sort(key=coordinates_dictionaries_comparison)  # sort by latitude then longitude
    return pixel_values
