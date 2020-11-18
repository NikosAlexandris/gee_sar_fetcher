def compose_sentinel1_data(
        start_date,
        end_date,
        geometry,
        scale,
        crs,
        pass_direction=ASCENDING,
        statistic=MEAN,
    ):
    '''
    Composes an image from an ImageCollection using input parameters and return data as a tuple of header and values.

    Parameters
    ----------
    start_date : str
        str following the pattern ``'yyyy-mm-dd'`` describing the start date of
        the time interval

    end_date : str
        str following the pattern ``'yyyy-mm-dd'`` describing the end date of
        the time interval

    geometry : ee.Geometry
        Geometry object defining the area of process

    scale : int
        Scale parameters of the getRegion() function. Defaulting at ``20``,
        change it to change the scale of the final data points. The highest,
        the lower the spatial resolution. Should be at least ``10``.

    pass_direction : str, optional
        Defines the pass direction to set for the data retrieval process

    Returns
    -------
    (val_header, val) : tuple
        val_header corresponds to the ``list of str`` describing the fields of
        the val array. The val array is a ``list`` of data records, each
        represented as a ``list`` of the same size as the val_header array.
    '''
    filtered_sentinel1_data = filter_sentinel1_data(
            start_date=start_date,
            end_date=end_date,
            geometry=geometry,
            pass_direction=pass_direction
    )
    values_vv = (filtered_sentinel1_data
              .select(VV)
              .reduce(statistic)
              .sample(
                  region=geometry,
                  scale=scale,
                  projection=crs,
                  geometries=True,
                  dropNulls=False,
              )
              .getInfo()
    )
    values_vh = (filtered_sentinel1_data
              .select(VH)
              .reduce(statistic)
              .sample(
                  region=geometry,
                  scale=scale,
                  projection=crs,
                  geometries=True,
                  dropNulls=False,
              )
              .getInfo()
    )
    header = ([
                'longitude',
                'latitude',
                'start_date',
                'end_date',
                VV,
                VH]
    )
    vv = []
    for feature in values_vv['features']:
        coordinates = feature['geometry']['coordinates']
        feature_property = feature['properties']
        value_vv = feature_property.get(VV + '_' + statistic)
        vv.extend([coordinates + [value_vv]])
    vh = []
    for feature in values_vh['features']:
        coordinates = feature['geometry']['coordinates']
        feature_property = feature['properties']
        value_vh = feature_property.get(VH + '_' + statistic)
        vh.extend([coordinates + [value_vh]])
        vh.extend([value_vh])
    values = [
        vv[idx] +
        [start_date] +
        [end_date] +
        [vh[idx]]
        for idx in range(len(vv))
    ]
    return (header, values)

def compose(
    top_left=None,
    bottom_right=None,
    coordinates=None,
    start_date: datetime = date.today()-timedelta(days=365),
    end_date: datetime = date.today(),
    ascending: bool = True,
    scale: int = 10,
    crs: str = 'EPSG:4326',
    statistic: str = 'mean',
    n_jobs: int = 1,
):
    '''Fetches a composite of SAR data in the form of a dictionnary with image data as well as timestamps

    Parameters
    ----------
    top_left : tuple of float, optional
        Top left coordinates (lon, lat) of the Region

    bottom_right : tuple of float, optional
        Bottom right coordinates (lon, lat) of the Region

    coordinates : tuple of tuple of float or list of list of float, optional
        If `top_left` and `bottom_right` are not specified, we expect `coordinates`
        to be a list (resp. tuple) of the form ``[top_left, bottom_right]``
        (resp. ``(top_left, bottom_right)``)

    start_date : datetime.datetime, optional
        First date of the time interval

    end_date : datetime.datetime, optional
        Last date of the time interval

    ascending : boolean, optional
        The trajectory to use when selecting data

    scale : int, optional
        Scale parameters of the getRegion() function. Defaulting at ``20``,
        change it to change the scale of the final data points. The highest,
        the lower the spatial resolution. Should be at least ``10``.

    statistic : str
        The descriptive statistic as per Google Earth Engine's reducers.
    n_jobs : int, optional
        Set the parallelisation factor (number of threads) for the GEE data
        access process. Set to 1 if no parallelisation required.

    Returns
    -------
    `dict`
        Dictionnary with two keys:

            ``"stacks"``
                4-D array containing db intensity measure (`numpy.ndarray`),
                ``(height, width, time_series_length, pol_count)``

            ``"coordinates"``
                3-D array containg coordinates where ``[:,:,0]`` provides
                access to latitude and ``[:,:,1]`` provides access to
                longitude, (`numpy.ndarray`), ``(height, width, 2)``

            ``"timestamps"``
                list of acquisition timestamps of size (time_series_length,)
                (`list of str`)

            ``"metadata"``
                Dictionnary describing data for each axis of the stack and the
                coordinates
    '''
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

    # date_intervals = get_date_interval_array(start_date, end_date)
    pass_direction = ASCENDING if ascending else DESCENDING

    if (top_left is not None):
        list_of_coordinates = [make_polygon(top_left, bottom_right)]
    else:
        list_of_coordinates = [coordinates]

    # retrieving the number of pixels per image
    try:
        polygon = ee.Geometry.Polygon(list_of_coordinates)
        sentinel_1_roi = fetch_sentinel1_data(
            start_date=date_intervals[0][0],
            end_date=date_intervals[-1][1],
            geometry=polygon,
            pass_direction=pass_direction,
        )

    except Exception as e:
        # If the area is found to be too big
        if (str(e) == "ImageCollection.getRegion: No bands in collection."):
            raise ValueError(
                "No bands found in collection. Orbit incorrect for localisation, please visit https://sentinel.esa.int/web/sentinel/missions/sentinel-1/observation-scenario for more info.")
        total_count_of_pixels = retrieve_max_pixel_count_from_pattern(str(e))
        if top_left is not None:
            list_of_coordinates = tile_coordinates(
                total_count_of_pixels, (top_left, bottom_right))
        else:
            list_of_coordinates = tile_coordinates(
                total_count_of_pixels, coords)

    ###################################
    ## RETRIEVING COORDINATES VALUES ##
    ## FOR EACH DATE INTERVAL        ##
    ###################################
    print(f'Region sliced in '
           '{len(list_of_coordinates)} subregions.'
    )
    def _get_zone_between_dates(start_date, end_date, polygon, scale, crs, pass_direction):
        try:
            val_header, val = fetch_sentinel1_data(
                start_date=start_date,
                end_date=end_date,
                geometry=polygon,
                pass_direction=pass_direction,
                scale=scale,
                crs=crs,
            )
            vals.extend(val)

            if len(headers) == 0:
                headers.extend(val_header)

        except Exception as e:
            pass

    for coordinates in tqdm(list_of_coordinates):
        vals = []
        headers = []
        subregion = ee.Geometry.Polygon([coordinates])
        # Fill vals with values.
        # TODO: Evaluate eventuality to remove shared memory requirement and to exploit automatic list building from Joblib
        Parallel(n_jobs=n_jobs, require='sharedmem')(delayed(_get_zone_between_dates)(sub_start_date, sub_end_date, polygon, scale, crs, pass_direction) for sub_start_date, sub_end_date in date_intervals)

        print("# of values:", len(vals))
        print("# of headers:", len(headers))
        dictified_vals = [dict(zip(headers, values)) for values in vals]
        print("# of dictified_vals:", len(dictified_vals))
        per_coord_dict = populate_coordinates_dictionary(dictified_values=dictified_vals)
        print("# of per_coord_dict:", len(per_coord_dict))

    # per_coord_dict is a dictionnary matching to each coordinate key its values through time as well as its timestamps

    ##############################
    ## BUILDING TEMPORAL IMAGES ##
    ##############################

    pixel_values = [per_coord_dict[k] for k in per_coord_dict.keys()]
    print("# of pixel_values:", len(pixel_values))
    cmp_coordinates = cmp_to_key(cmp_coords)
    pixel_values.sort(key=cmp_coordinates)  # sorting pixels by latitude then longitude
    print("# of sorted pixel_values:", len(pixel_values))
    width, height = define_image_shape(pixel_values)
    print(f"Generating image of shape (width x height) {width} x {height}")
    def _update_img(pixel_value):
        vv = []
        vh = []
        for timestamp in timestamps:

            indexes = np.argwhere(
                np.array([datetime.fromtimestamp(p_t).date() for p_t in pixel_value["timestamps"]]) == timestamp
            )
            vv.append(np.nanmean(
                np.array(pixel_value["VV"], dtype=float)[indexes]))
            vh.append(np.nanmean(
                np.array(pixel_value["VH"], dtype=float)[indexes]))
        return [vv, vh]

    print("Height:", height)
    print("Width:", width)
    indexes = [(i,j) for i in range(height) for j in range(width)]
    vals = Parallel(n_jobs=n_jobs)(
        delayed(_update_img)(pixel_values[i*width + j]) for (i,j) in tqdm(indexes)
    )
    img = np.array(vals).reshape((height, width, 2, len(timestamps)))
    lats, lons = tuple(zip(*[(p["lat"], p["lon"]) for p in pixel_values]))
    lats = np.array(lats).reshape((height, width))
    lons = np.array(lons).reshape((height, width))
    coordinates = np.zeros((height, width,2))
    coordinates[:,:,0] = lats
    coordinates[:,:,1] = lons

    return {
        "stack": img,
        "coordinates": coordinates,
        "metadata": {
            "stack": {
                "axis_0": "height",
                "axis_1": "width",
                "axis_2": "polarisations (0:VV, 1:VH)",
            },
            "coordinates": {
                "axis_0": "height",
                "axis_1": "width",
                "axis_2": "0:latitude; 1:longitude",
            }
        }
    }

