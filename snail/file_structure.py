'''
This library defines methods to work with the midi header and midi tracks in a file
'''
from logbook import Logger
import struct

log = Logger('snail')


DEFAULT_MIDI_HEADER_LEN = 14


def parse_file_header(infile):
    '''
Receives a file like object; parses and returns parts of the midi header

:param infile: a file like object pointed at the first byte after the header
:param header_len: in bytes, in addition to the 4 for the declaration and the 4 for this number
:param midi_format: the midi format (0, 1 or 2) http://en.wikipedia.org/wiki/MIDI#Standard_MIDI_files
:param track_count: the number of tracks specified by the header
:param resolution: the PPQN http://en.wikipedia.org/wiki/Pulses_per_quarter_note
    '''
    try:
        # First four bytes are MIDI header declaration
        midi_header_declaration = infile.read(4)
        if midi_header_declaration != b'MThd':
            err_text = "This is not a midi header - wrong declaration"
            log.critical(err_text)
            raise TypeError(err_text)

        # next four bytes are header size in bytes
        header_len = struct.unpack(">L", infile.read(4))[0]  # always a tuple
        log.info('Header size: 8 + {}'.format(header_len))

        # next two bytes specify the format version
        midi_format = struct.unpack(">H", infile.read(2))[0]  # always a tuple
        log.info('Midi file format: {}'.format(midi_format))
        if midi_format not in (0, 1, 2):
            err_text = "This is not a midi header - incorrect midi format"
            log.critical(err_text)
            raise TypeError(err_text)

        # next two bytes specify the number of tracks
        track_ct = 0
        track_ct = struct.unpack(">H", infile.read(2))[0]  # always a tuple
        log.info('Number of tracks: {}'.format(track_ct))

        # next two bytes specify the resolution/PPQ/Parts Per Quarter
        # (in other words, how many ticks per quater note)
        resolution = 0
        resolution = struct.unpack(">H", infile.read(2))[0]  # always a tuple
        log.info('Resolution: {}'.format(resolution))

        # NOTE: the assumption is that any remaining bytes
        # in the header are padding
        # NOTE: remember the 4 from the declaration and 4 for the size
        if (header_len + 8) > DEFAULT_MIDI_HEADER_LEN:
            infile.read(header_len + 8 - DEFAULT_MIDI_HEADER_LEN)

    except Exception as ex:
        log.critical(ex)
        raise ex

    return infile, header_len, midi_format, track_ct, resolution


def build_file_header(midi_format, track_ct, resolution):
    '''
Receives info regarding a midi file

:param midi_format: the midi format (0, 1 or 2) http://en.wikipedia.org/wiki/MIDI#Standard_MIDI_files
:param track_count: the number of tracks specified by the header
:param resolution: the PPQN http://en.wikipedia.org/wiki/Pulses_per_quarter_note

:returns a :class:`bytearray` len 14
    '''
    try:
        rslt_li = []
        # First four bytes are MIDI header declaration
        rslt_li.append(b'MThd')

        # next four bytes are header size in bytes
        #  a len of 6 more bytes is standard
        rslt_li.append(struct.pack(">L", 6))

        # next two bytes specify the format version
        if midi_format not in (0, 1, 2):
            err_text = "{} is not a valid midi format - only (0, 1 or 2)".format(midi_format)
            log.critical(err_text)
            raise TypeError(err_text)

        rslt_li.append(struct.pack(">H", midi_format))

        # next two bytes specify the number of tracks
        rslt_li.append(struct.pack(">H", track_ct))

        # next two bytes specify the resolution/PPQ/Parts Per Quarter
        # (in other words, how many ticks per quater note)
        rslt_li.append(struct.pack(">H", resolution))

    except Exception as ex:
        log.critical(ex)
        raise ex
    btye_li = b''.join(rslt_li)

    return btye_li


def parse_track_header(infile):
    '''
:param infile: a file like object

returns:
infile: a file like object pointed at the first byte after the header
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

    return infile, track_len

def build_track_header(track_len):
    '''
:param track_len: in bytes, in addition to the 4 for the declaration and the 4 for this number

:returns: a :class:`bytearray` 8 bytes long
    '''
    return b''.join([b'MTrk', struct.pack('>L', track_len)])


def get_track_iter(infile):
    '''
:param infile: a file like object; just before a track

returns:
    infile: a file like object
    track_iter: an :class:`iterator` for the remaining bytes in a track
    '''
    pass
