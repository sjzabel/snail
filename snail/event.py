'''
This library defines methods to work with midi events
'''
from logbook import Logger
import struct
from snail import vlq

log = Logger('snail')


def parse_event(byte_iter):
    '''
    :param byte_iter: a :class:`iterator` for the remaining bytes in a track

    returns:
        an :class:`dict` containing info on the event
    '''
    ev = {} #event
    ev['tick'] = vlq.read(byte_iter)
    sysmsg = ev['system_message'] = next(byte_iter)
