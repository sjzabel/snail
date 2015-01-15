"""
File: sysex_events.py
Author: Stephen J. Zabel
Email: sjzabel@gmail.com
Github: https://github.com/sjzabel
Description: This file defines helpers for midi sysex events and sysex events
"""


SYSEX_EVENT_CODE = 0xF0


def is_sysex_event(event_code):
    '''
    :param event_code: the midi event code
    returns: boolean
    '''
    return event_code == SYSEX_EVENT_CODE


SYSEX_EVENT_DICT = {
    0x00: {
		'name': "Sequence Number",
		'parse': 'parse_ascii',
	},
}


def parse_event(event_d, track_iter):
    '''
    :param event_d: the event dict with the information know so far
    :param track_iter: a :class:`iterator` for the remaining bytes in a track

    returns:
        an :class:`dict` containing info on the event
    '''
    ev['event_type'] = 'sysex'


    return ev
