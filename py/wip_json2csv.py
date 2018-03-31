def flattenjson( b, delim ):
    val = {}
    for i in b.keys():
        if isinstance( b[i], dict ):
            get = flattenjson( b[i], delim )
            for j in get.keys():
                val[ i + delim + j ] = get[j]
        else:
            val[i] = b[i]

    return val


# flattenjson( {
#     "pk": 22,
#     "model": "auth.permission",
#     "fields": {
#       "codename": "add_message",
#       "name": "Can add message",
#       "content_type": 8
#     }
#   }, "__" )
# is
#
# {
#     "pk": 22,
#     "model": "auth.permission',
#     "fields__codename": "add_message",
#     "fields__name": "Can add message",
#     "fields__content_type": 8
# }

# After applying this function to each dict in the input array of JSON objects:

input = map( lambda x: flattenjson( x, "__" ), input )
# and finding the relevant column names:

columns = [ x for row in input for x in row.keys() ]
columns = list( set( columns ) )
it's not hard to run this through the csv module:

with open( fname, 'wb' ) as out_file:
    csv_w = csv.writer( out_file )
    csv_w.writerow( columns )

    for i_r in input:
        csv_w.writerow( map( lambda x: i_r.get( x, "" ), columns ) )
