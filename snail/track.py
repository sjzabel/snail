'''
This library defines methods to work with midi tracks in a file
'''
from logbook import Logger
import struct

log = Logger('snail')


def parse_track_header(infile):
    '''
    :param infile: a file like object

    returns:
        track_len: in bytes, in addition to the 4 for the declaration and the 4 for this number
    '''
    try:
        # First four bytes are MIDI track declaration
        midi_track_declaration = infile.read(4)
        if midi_track_declaration != b'MTrk':
            err_text = "This is not a midi track - wrong declaration"
            log.critical(err_text)
            raise TypeError(err_text)

        # next four bytes are track size in bytes
        track_len = struct.unpack(">L", infile.read(4))[0]  # always a tuple
        log.info('remaining track size: {}'.format(track_len))

    except Exception as ex:
        log.critical(ex)
        raise ex

    return track_len

def build_track_header(track_len):
    '''
    :param track_len: in bytes, in addition to the 4 for the declaration and the 4 for this number

    returns:
        a :class:`bytearray` 8 bytes long
    '''
    return b''.join([b'MTrk', struct.pack('>L', track_len)])


def get_track_iter(infile):
    '''
    Parse track header and return an iterator for the remaining len
    This is a convient way of knowing that you have read the entire track.

    :param infile: a file like object; just before a track

    returns:
        a :class:`iterator` for the remaining bytes in a track
    '''
    track_len = parse_track_header(infile)
    return iter(infile.read(track_len))
