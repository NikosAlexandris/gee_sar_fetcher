import pyproj
SINUSOIDAL = {'proj' : 'sinu', 'R' : 6371007.181000, 'units' : 'm'}

def degrees_to_sinusoidal(west, north, east, south):
    """
    """
    to_sinusoidal = pyproj.Proj(SINUSOIDAL)
    north_west = to_sinusoidal(west, north) # top_left
    east_south = to_sinusoidal(east, south) # bottom_right
    return north_west[0], north_west[1], east_south[0], east_south[1]
