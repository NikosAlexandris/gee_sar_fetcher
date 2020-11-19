from .constants import VV
from .constants import VH

def strucure_data(
        image,
        coordinates,
    ):
    """
    """
    return {
        'stack': image,
        'coordinates': coordinates,
        'metadata': {
            'stack': {
                'axis_0': 'height',
                'axis_1': 'width',
                'axis_2': {
                    'polarisations': {
                        0:VV,
                        1:VH
                    },
                },
            },
            'coordinates': {
                'axis_0': 'height',
                'axis_1': 'width',
                'axis_2': '0:latitude; 1:longitude',
            }
        }
    }

