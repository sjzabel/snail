from snail import file_structure
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
            file_structure.parse_track_header(infile)

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

        infile, header_len = file_structure.parse_track_header(infile)
        self.assertEqual(header_len, 4294967295)

    def test_build_track_header_correctly(self):
        infile = io.BytesIO(file_structure.build_track_header(4294967295))

        infile, header_len = file_structure.parse_track_header(infile)
        self.assertEqual(header_len, 4294967295)
