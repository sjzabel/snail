"""
File: event.py
Author: Stephen J. Zabel
Email: sjzabel@gmail.com
Github: https://github.com/sjzabel
Description: This library defines methods to work with midi events
"""
from logbook import Logger
import struct
from snail import vlq
from snail import sysex_event
from snail import meta_event

log = Logger('snail')


def parse_event(track_iter):
    '''
    :param track_iter: a :class:`iterator` for the remaining bytes in a track

    returns:
        an :class:`dict` containing info on the event
    '''
    ev = {} #event
    ev['tick'] = vlq.read(track_iter)
    sysmsg = ev['system_message'] = next(track_iter)

