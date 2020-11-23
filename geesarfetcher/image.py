import numpy
from tqdm import tqdm
from .constants import VV
from .constants import VH
from .coordinates import northing_and_easting


def generate_image(
        height,
        width,
        pixel_values,
        unique_northings,
        unique_eastings,
    ):
    """
    """
    northings_dictionary = {
            unique_northings[i]: i
            for i in range(len(unique_northings))
    }
    eastings_dictionary = {
            unique_eastings[i]: i
            for i in range(len(unique_eastings))
    }
    image = numpy.full((height, width, 2), fill_value=numpy.nan)
    print(f'Generating image of shape (height x width) {height, width}')
    # ------------------------------------------------------------- REFACTOR ---
    for p in tqdm(pixel_values):
        x, y = latitudes_dictionary[p["lat"]], longitudes_dictionary[p["lon"]]
        vv = []
        vh = []
        for timestamp in timestamps:

            indexes = np.argwhere(
                np.array([datetime.fromtimestamp(p_t).date() for p_t in p["timestamps"]]) == timestamp
            )
            vv.append(np.nanmean(
                np.array(p["VV"], dtype=float)[indexes]))
            vh.append(np.nanmean(
                np.array(p["VH"], dtype=float)[indexes]))

        image[x, y, 0, :] = vv
        image[x, y, 1, :] = vh
    # ------------------------------------------------------------- REFACTOR ---
    return image


def generate_composite_image(
        pixel_values,
        unique_northings,
        unique_eastings,
    ):
    """
    """
    height = len(unique_northings)
    width = len(unique_eastings)
    northings_dictionary = {
            unique_northings[i]: i
            for i in range(height)
    }
    eastings_dictionary = {
            unique_eastings[i]: i
            for i in range(width)
    }
    image = numpy.full((height, width, 2), fill_value=numpy.nan)
    print(f'Generating image of shape (height x width) {height, width}')
    for pixel_value in tqdm(pixel_values):
        northing, easting = northing_and_easting(pixel_value)
        x = northings_dictionary[pixel_value[northing]]
        y = eastings_dictionary[pixel_value[easting]]
        image[x, y, 0] = numpy.nanmean(pixel_value[VV], dtype=float)
        image[x, y, 1] = numpy.nanmean(pixel_value[VH], dtype=float)
    return image
