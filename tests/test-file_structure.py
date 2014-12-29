from snail import file_structure
from unittest.mock import MagicMock
import io
import logbook
import re
import struct
import unittest


class TestFileStructure(unittest.TestCase):
    def setUp(self):
        self.log_handler = logbook.TestHandler()
        self.log_handler.push_thread()
        self.stderrhndlr = logbook.StderrHandler(level='DEBUG', bubble=True)
        # add with self.stderrhndlr.applicationbound():
        # to see logging

    def tearDown(self):
        self.log_handler.pop_thread()

    def test_parse_header_raises_declaration_error(self):
        infile = io.BytesIO(b'NOTMThd')

        with self.assertRaises(TypeError):
            file_structure.parse_header(infile)

        self.assertTrue(self.log_handler.has_critical(re.compile('wrong declaration'), channel='snail'))

    def test_parse_header_reads_declaration_correctly(self):
        infile = io.BytesIO(b'MThd')

        self.assertFalse(self.log_handler.has_critical(re.compile('wrong declaration'), channel='snail'))

    def test_parse_header_reads_header_len_correctly(self):
        byte_li = [
            b'MThd',
            struct.pack('>L', 6),
            struct.pack('>H', 1),
            struct.pack('>H', 4),
            # 'H' format requires 0 <= number <= 65535
            struct.pack('>H', 65535),
        ]
        infile = io.BytesIO(b''.join(byte_li))

        infile, header_len, midi_format, track_ct, resolution = file_structure.parse_header(infile)
        self.assertEqual(header_len, 6)

    def test_parse_header_returns_midi_format_error(self):
        byte_li = [
            b'MThd',
            struct.pack('>L', 6),
            struct.pack('>H', 5),
            struct.pack('>H', 4),
            struct.pack('>H', 65535),
        ]
        infile = io.BytesIO(b''.join(byte_li))

        with self.assertRaises(TypeError):
            file_structure.parse_header(infile)

        self.assertTrue(self.log_handler.has_critical(re.compile('incorrect midi format'), channel='snail'))

    def test_parse_header_returns_midi_format_correctly(self):
        byte_li = [
            b'MThd',
            struct.pack('>L', 6),
            struct.pack('>H', 1),
            struct.pack('>H', 4),
            struct.pack('>H', 65535),
        ]
        infile = io.BytesIO(b''.join(byte_li))

        infile, header_len, midi_format, track_ct, resolution = file_structure.parse_header(infile)
        self.assertEqual(midi_format, 1)

    def test_parse_header_returns_file_obj_correctly_for_default_len(self):
        byte_li = [
            b'MThd',
            struct.pack('>L', 6),
            struct.pack('>H', 1),
            struct.pack('>H', 4),
            struct.pack('>H', 65535),
        ]
        infile = io.BytesIO(b''.join(byte_li))

        infile, header_len, midi_format, track_ct, resolution = file_structure.parse_header(infile)
        self.assertTrue(infile.tell(), file_structure.DEFAULT_MIDI_HEADER_LEN)

    def test_parse_header_returns_file_obj_correctly_for_padded_len(self):
        byte_li = [
            b'MThd',
            struct.pack('>L', 16),
            struct.pack('>H', 1),
            struct.pack('>H', 4),
            struct.pack('>H', 65535),
            b'PADDING YO',
        ]
        infile = io.BytesIO(b''.join(byte_li))

        infile, header_len, midi_format, track_ct, resolution = file_structure.parse_header(infile)
        self.assertTrue(infile.tell(), file_structure.DEFAULT_MIDI_HEADER_LEN + 10)

    def test_parse_header_returns_track_ct_correctly(self):
        byte_li = [
            b'MThd',
            struct.pack('>L', 6),
            struct.pack('>H', 1),
            struct.pack('>H', 4),
            struct.pack('>H', 65535),
        ]
        infile = io.BytesIO(b''.join(byte_li))

        infile, header_len, midi_format, track_ct, resolution = file_structure.parse_header(infile)
        self.assertTrue(track_ct, 4)

    def test_parse_header_returns_resolution_correctly(self):
        byte_li = [
            b'MThd',
            struct.pack('>L', 6),
            struct.pack('>H', 1),
            struct.pack('>H', 4),
            struct.pack('>H', 65535),
        ]
        infile = io.BytesIO(b''.join(byte_li))

        infile, header_len, midi_format, track_ct, resolution = file_structure.parse_header(infile)
        self.assertTrue(resolution, 65535)
