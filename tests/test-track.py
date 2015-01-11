from snail import track
from unittest.mock import MagicMock
import io
import logbook
import re
import struct
import unittest


class TestFileStructureTrackHeader(unittest.TestCase):
    def setUp(self):
        self.log_handler = logbook.TestHandler()
        self.log_handler.push_thread()
        self.stderrhndlr = logbook.StderrHandler(level='DEBUG', bubble=True)
        # add with self.stderrhndlr.applicationbound():
        # to see logging

    def tearDown(self):
        self.log_handler.pop_thread()

    def test_parse_track_header_raises_declaration_error(self):
        infile = io.BytesIO(b'NOTMTrk')

        with self.assertRaises(TypeError):
            track.parse_track_header(infile)

        self.assertTrue(self.log_handler.has_critical(re.compile('wrong declaration'), channel='snail'))

    def test_parse_track_header_reads_declaration_correctly(self):
        infile = io.BytesIO(b'MTrk')

        self.assertFalse(self.log_handler.has_critical(re.compile('wrong declaration'), channel='snail'))

    def test_parse_track_header_reads_track_len_correctly(self):
        byte_li = [
            b'MTrk',
            # 'L' format requires 0 <= number <= 4294967295
            struct.pack('>L', 4294967295),
        ]
        infile = io.BytesIO(b''.join(byte_li))

        header_len = track.parse_track_header(infile)
        self.assertEqual(header_len, 4294967295)

    def test_build_track_header_correctly(self):
        infile = io.BytesIO(track.build_track_header(4294967295))

        header_len = track.parse_track_header(infile)
        self.assertEqual(header_len, 4294967295)

    def test_get_track_iter(self):
        byte_li = [
            b'MTrk',
            struct.pack('>L', 5),
            b'test' * 50,
        ]
        infile = io.BytesIO(b''.join(byte_li))

        track_iter = track.get_track_iter(infile)
        self.assertEqual('testt', ''.join([chr(b) for b in track_iter]))
        self.assertEqual(8 + 5, infile.tell())  # don't forget about the header bytes
