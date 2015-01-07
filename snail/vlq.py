'''
Utilities to handle Variable Length Quantity midi data

Heavily borrowed from python-midi's midi.util class and tested for
python >= 3.4

http://en.wikipedia.org/wiki/Variable-length_quantity
'''
def read(byte_iter):
    '''
    Parses a VLQ

    :param byte_iter: an iterator over a byte array

    returns:
        quantity (a potentially large number)

    raises:
        StopIteration if the byte_iter has no more to read
    '''

    has_next_byte = True
    value = None
    while has_next_byte:
        chr = next(byte_iter)

        # is the hi-bit set?
        if not (chr & 0x80):
            # no next BYTE
            has_next_byte = False
        # mask out the 8th bit
        chr = chr & 0x7f
        # shift last value up 7 bits
        value = value << 7
        # add new value
        value += chr
    return value

def write(value):
    chr1 = chr(value & 0x7F)
    value >>= 7
    if value:
        chr2 = chr((value & 0x7F) | 0x80)
        value >>= 7
        if value:
            chr3 = chr((value & 0x7F) | 0x80)
            value >>= 7
            if value:
                chr4 = chr((value & 0x7F) | 0x80)
                res = chr4 + chr3 + chr2 + chr1
            else:
                res = chr3 + chr2 + chr1
        else:
            res = chr2 + chr1
    else:
        res = chr1
    return res
