import numpy
from tqdm import tqdm
from .constants import VV
from .constants import VH


def generate_image(
        height,
        width,
        pixel_values,
        unique_latitudes,
        unique_longitudes,
    ):
    """
    """
    latitudes_dictionary = {
            unique_latitudes[i]: i
            for i in range(len(unique_latitudes))
    }
    longitudes_dictionary = {
            unique_longitudes[i]: i
            for i in range(len(unique_longitudes))
    }
    image = numpy.full((height, width, 2), fill_value=numpy.nan)
    print(f'Generating image of shape (height x width) {height, width}')
    for pixel_value in tqdm(pixel_values):
        x = latitudes_dictionary[pixel_value['lat']]
        y = longitudes_dictionary[pixel_value['lon']]
        image[x, y, 0] = numpy.nanmean(pixel_value[VV], dtype=float)
        image[x, y, 1] = numpy.nanmean(pixel_value[VH], dtype=float)
    return image
