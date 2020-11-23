from .constants import VV
from .constants import VH

def strucure_data(
def strucure_composite_data(
        image,
        coordinates,
        timestamps,
    ):
    """
    """
    return {
        'stack': image,
        'coordinates': coordinates,
        'timestamps': timestamps,
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
            },
            'timestamps': {
                'axis_0': 'start_date',
                'axis_1': 'end_date',
            },
        }
    }

