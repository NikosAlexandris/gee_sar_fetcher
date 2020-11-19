from .messages import VALUE_ERROR_NO_COORDINATES

def assert_inputs(coordinates, top_left, bottom_right, start_date, end_date):
    """
    Assert input parameters to compose()
    """
    assert(coordinates is None or (
        (
            type(coordinates) == list
            or type(coordinates) == tuple
        )
        and len(coordinates) == 2)
        and len(coordinates[0]) == len(coordinates[1])
        and len(coordinates[0]) == 2
    )
    assert(
            (
                top_left is None
                and bottom_right is None
            )
            or (
                type(top_left) == type(bottom_right)
                and (
                    type(top_left) == tuple
                    or type(top_left) == list)
            )
            and len(top_left) == len(bottom_right)
            and len(top_left) == 2
    )
    assert(start_date is not None)
    assert(end_date is not None)
    assert(end_date > start_date)

    if (top_left is not None
        and bottom_right is not None
        and coordinates is not None):
        raise ValueError(VALUE_ERROR_NO_COORDINATES)
