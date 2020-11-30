# coordinates = composite['coordinates']
# data = composite['stack']
# dstack = numpy.dstack((coordinates, data))
# sample = dstack[0, :]
# dtype = numpy.dtype([('x', np.float32), ('y', np.float32),('VV', np.float32), ('VH', np.float32)])
# final = np.array(np.rec.fromarrays(sample.transpose(), names=dtype.names).astype(dtype=dtype).tolist(), dtype=dtype)
# new_dtype = np.dtype(final.dtype.descr + [('Start', '<U10'), ('End', '<U10')])
# b = np.zeros(final.shape, dtype=new_dtype)
# b['x'] = final['x']
# b['y'] = final['y']
# b['VV'] = final['VV']
# b['VH'] = final['VH']
# b['Start'] = start_date
# b['End'] = end_date
# CSV_HEADER = (',').join(['Northing,Easting,VV,VH,Start,End'])
# numpy.savetxt('b.csv', b, delimiter=',', fmt=['%f' , '%f', '%f', '%f', '%s', '%s'], header=CSV_HEADER, comments='')


DATA_TYPES = numpy.dtype([('x', np.float32), ('y', np.float32),('VV', np.float32), ('VH', np.float32)])
NEW_DATA_TYPES = [('Start', (np.str, 8)), ('End', (np.str, 8))]
DELIMITER = ','
FIELD_FORMATS = ['%f' , '%f', '%f', '%f', '%s', '%s']

# get data
coordinates = sentinel_1_composite['coordinates']
data = sentinel_1_composite['stack']
stack = numpy.dstack((coordinates, data))
stack = stack[0, 100:110]  # comment out to do all data

# convert to structured array
structured_array = structure_ndarray(stack, dtypes=DATA_TYPES)

# build final structured array
final_data_types = np.dtype(structured_array.dtype.descr + NEW_DATA_TYPES)
final_structured_array = np.zeros(structured_array.shape, dtype=final_data_types)

# copy over the existing data
for field in structured_array.dtype.names:
    final_structured_array[field] = structured_array[field]

# fill-in start and end dates
final_structured_array['Start'] = start_date
final_structured_array['End'] = end_date

# write out CSV
numpy.savetxt(filename,
        final_structured_array,
        delimiter=DELIMITER,
        fmt=FIELD_FORMATS,
        header=header,
        footer='',
        comments='',
)
