from boa.builtins import concat, list, range, substr

def deserialize_bytearray(data):

    # ok this is weird.  if you remove this print statement, it stops working :/
    print("deserializing data...")

    # get length of length
    collection_length_length = substr(data, 0, 1)

    # get length of collection
    collection_len = substr(data, 1, collection_length_length)

    # create a new collection
    new_collection = list(length=collection_len)

    # calculate offset
    offset = 1 + collection_length_length

    for i in range(0, collection_len):

        # get the data length length
        itemlen_len = substr(data, offset, 1)

        # get the length of the data
        item_len = substr(data, offset+1, itemlen_len)

        start = 1 + itemlen_len
        end = start + item_len

        # get the data
        item = substr(data, offset + start, item_len)

        # store it in collection
        print(item)
        new_collection[i] = item

        # trim the data
        offset = offset + itemlen_len + item_len + 1

    return new_collection



def serialize_array(items):

    # serialize the length of the list
    itemlength = serialize_var_length_item(items)

    output = itemlength

    # now go through and append all your stuff
    for item in items:

        # get the variable length of the item
        # to be serialized
        itemlen = serialize_var_length_item(item)

        # add that indicator
        output = concat(output, itemlen)

        # now add the item
        output = concat(output, item)

    # return the stuff
    return output


def serialize_var_length_item(item):

    # get the length of your stuff
    stuff_len = len(item)

    # now we need to know how many bytes the length of the array
    # will take to store

    # this is one byte
    if stuff_len <= 255:
        byte_len = b'\x01'
    # two byte
    elif stuff_len <= 65535:
        byte_len = b'\x02'
    # hopefully 4 byte
    else:
        byte_len = b'\x04'

    out = concat(byte_len, stuff_len)

    return out
