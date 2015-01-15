"""
File: vlq.py
Author: Stephen J. Zabel
Email: sjzabel@gmail.com
Github: https://github.com/sjzabel
Description: Utilities to handle Variable Length Quantity midi data

Heavily borrowed from python-midi's midi.util class and tested for
python >= 3.4

http://en.wikipedia.org/wiki/Variable-length_quantity
"""



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
        char = next(byte_iter)

        # is the hi-bit set?
        if not (char & 0x80):
            # no next BYTE
            has_next_byte = False
        # mask out the 8th bit
        char = char & 0x7f
        # shift last value up 7 bits
        value = value << 7
        # add new value
        value += char
    return value

def write(value):
    char1 = chr(value & 0x7F)
    value >>= 7
    if value:
        char2 = chr((value & 0x7F) | 0x80)
        value >>= 7
        if value:
            char3 = chr((value & 0x7F) | 0x80)
            value >>= 7
            if value:
                char4 = chr((value & 0x7F) | 0x80)
                res = char4 + char3 + char2 + char1
            else:
                res = char3 + char2 + char1
        else:
            res = char2 + char1
    else:
        res = char1
    return res
