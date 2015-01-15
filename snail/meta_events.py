"""
File: meta_events.py
Author: Stephen J. Zabel
Email: sjzabel@gmail.com
Github: https://github.com/sjzabel
Description: This file defines helpers for midi meta events and meta events
"""


META_EVENT_CODE = 0xFF


def is_meta_event(event_code):
    '''
    :param event_code: the midi event code
    returns: boolean
    '''
    return event_code == META_EVENT_CODE


META_EVENT_DICT = {
    0x00: {
		'name': "Sequence Number",
		'parse': 'parse_ascii',
	},
    0x01: {
		'name': "Text Event",
		'parse': 'parse_ascii',
	},
    0x02: {
		'name': "Copyright Notice",
		'parse': 'parse_ascii',
	},
    0x03: {
		'name': "Sequence or Track Name",
		'parse': 'parse_ascii',
	},
    0x04: {
		'name': "Instrument Name",
		'parse': 'parse_ascii',
	},
    0x05: {
		'name': "Lyric Text",
		'parse': 'parse_ascii',
	},
    0x06: {
		'name': "Marker Text",
		'parse': 'parse_ascii',
	},
    0x07: {
		'name': "Cue Point",
		'parse': 'parse_ascii',
	},
    0x08: {
		'name': "Program Name",
		'parse': 'parse_ascii',
	},
    0x20: {
		'name': "MIDI Channel Prefix Assignment",
		'parse': 'parse_ascii',
	},
    0x21: {
		'name': "MIDI Port or Cable",
		'parse': 'parse_ascii',
	},
    0x2E: {
		'name': "Track Loop",
		'parse': 'parse_ascii',
	},
    0x2F: {
		'name': "End of Track",
		'parse': 'parse_ascii',
	},
    0x51: {
		'name': "Tempo Setting",
		'parse': 'parse_ascii',
	},
    0x54: {
		'name': "SMPTE Offset",
		'parse': 'parse_ascii',
	},
    0x58: {
		'name': "Time Signature",
		'parse': 'parse_struct',
        'struct map': ['numerator', 'denominator', 'metronome', 'thirtyseconds']
	},
    0x59: {
		'name': "Key Signature",
		'parse': 'parse_struct',
        'struct map': ['alternatives', 'minor']
	},
    0x7F: {
		'name': "Sequencer Specific Event",
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
    ev['event_type'] = 'meta'


    return ev
