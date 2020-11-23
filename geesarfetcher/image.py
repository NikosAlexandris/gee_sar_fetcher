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
def generate_composite_image(
    for pixel_value in tqdm(pixel_values):
        northing, easting = northing_and_easting(pixel_value)
        x = northings_dictionary[pixel_value[northing]]
        y = eastings_dictionary[pixel_value[easting]]
        image[x, y, 0] = numpy.nanmean(pixel_value[VV], dtype=float)
        image[x, y, 1] = numpy.nanmean(pixel_value[VH], dtype=float)
    return image
