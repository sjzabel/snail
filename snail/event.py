"""
File: event.py
Author: Stephen J. Zabel
Email: sjzabel@gmail.com
Github: https://github.com/sjzabel
Description: This library defines methods to work with midi events
"""
from logbook import Logger
from snail import meta_event
from snail import sysex_event
from snail import vlq
import struct

log = Logger('snail')


def parse_event(track_iter):
    '''
    :param track_iter: a :class:`iterator` for the remaining bytes in a track

    returns:
        an :class:`dict` containing info on the event
    '''
    ev = {} #event
    ev['tick'] = vlq.read(track_iter)
    ev_cd = ev['event_code'] = next(track_iter)

    if meta_event.is_meta_event(ev_cd):
        ev = meta_event.parse_event(ev, track_iter)

    elif sysex_event.is_sysex_event(ev_cd):
        ev = sysex_event.parse_event(ev, track_iter)

    elif ev_cd < 0x80:
        # TODO: handle continuation events
        raise TypeError("We don't currently handle continuation events")

    else:
        # we are in "normal" events
        ev = parse_event(ev, track_iter)

    return ev

