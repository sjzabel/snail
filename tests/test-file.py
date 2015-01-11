from snail import file as midi_file
from unittest.mock import MagicMock
import io
import logbook
import re
import struct
import unittest


class TestFileStructureFileHeader(unittest.TestCase):
    def setUp(self):
        self.log_handler = logbook.TestHandler()
        self.log_handler.push_thread()
        self.stderrhndlr = logbook.StderrHandler(level='DEBUG', bubble=True)
        # add with self.stderrhndlr.applicationbound():
        # to see logging

    def tearDown(self):
        self.log_handler.pop_thread()

    def test_parse_file_header_raises_declaration_error(self):
        infile = io.BytesIO(b'NOTMThd')

        with self.assertRaises(TypeError):
            midi_file.parse_file_header(infile)

        self.assertTrue(self.log_handler.has_critical(re.compile('wrong declaration'), channel='snail'))

    def test_parse_file_header_reads_declaration_correctly(self):
        infile = io.BytesIO(b'MThd')

        self.assertFalse(self.log_handler.has_critical(re.compile('wrong declaration'), channel='snail'))

    def test_parse_file_header_reads_header_len_correctly(self):
        byte_li = [
            b'MThd',
            struct.pack('>L', 6),
            struct.pack('>H', 1),
            struct.pack('>H', 4),
            # 'H' format requires 0 <= number <= 65535
            struct.pack('>H', 65535),
        ]
        infile = io.BytesIO(b''.join(byte_li))

        header_len, midi_format, track_ct, resolution = midi_file.parse_file_header(infile)
        self.assertEqual(header_len, 6)

    def test_parse_file_header_returns_midi_format_error(self):
        byte_li = [
            b'MThd',
            struct.pack('>L', 6),
            struct.pack('>H', 5),
            struct.pack('>H', 4),
            struct.pack('>H', 65535),
        ]
        infile = io.BytesIO(b''.join(byte_li))

        with self.assertRaises(TypeError):
            midi_file.parse_file_header(infile)

        self.assertTrue(self.log_handler.has_critical(re.compile('incorrect midi format'), channel='snail'))

    def test_parse_file_header_returns_midi_format_correctly(self):
        byte_li = [
            b'MThd',
            struct.pack('>L', 6),
            struct.pack('>H', 1),
            struct.pack('>H', 4),
            struct.pack('>H', 65535),
        ]
        infile = io.BytesIO(b''.join(byte_li))

        header_len, midi_format, track_ct, resolution = midi_file.parse_file_header(infile)
        self.assertEqual(midi_format, 1)

    def test_parse_file_header_returns_file_obj_correctly_for_default_len(self):
        byte_li = [
            b'MThd',
            struct.pack('>L', 6),
            struct.pack('>H', 1),
            struct.pack('>H', 4),
            struct.pack('>H', 65535),
        ]
        infile = io.BytesIO(b''.join(byte_li))

        header_len, midi_format, track_ct, resolution = midi_file.parse_file_header(infile)
        self.assertEqual(infile.tell(), midi_file.DEFAULT_MIDI_HEADER_LEN)

    def test_parse_file_header_returns_file_obj_correctly_for_padded_len(self):
        byte_li = [
            b'MThd',
            struct.pack('>L', 16),
            struct.pack('>H', 1),
            struct.pack('>H', 4),
            struct.pack('>H', 65535),
            b'PADDING YO',
        ]
        infile = io.BytesIO(b''.join(byte_li))

        header_len, midi_format, track_ct, resolution = midi_file.parse_file_header(infile)
        self.assertEqual(infile.tell(), midi_file.DEFAULT_MIDI_HEADER_LEN + 10)

    def test_parse_file_header_returns_track_ct_correctly(self):
        byte_li = [
            b'MThd',
            struct.pack('>L', 6),
            struct.pack('>H', 1),
            struct.pack('>H', 4),
            struct.pack('>H', 65535),
        ]
        infile = io.BytesIO(b''.join(byte_li))

        header_len, midi_format, track_ct, resolution = midi_file.parse_file_header(infile)
        self.assertEqual(track_ct, 4)

    def test_parse_file_header_returns_resolution_correctly(self):
        byte_li = [
            b'MThd',
            struct.pack('>L', 6),
            struct.pack('>H', 1),
            struct.pack('>H', 4),
            struct.pack('>H', 65535),
        ]
        infile = io.BytesIO(b''.join(byte_li))

        header_len, midi_format, track_ct, resolution = midi_file.parse_file_header(infile)
        self.assertEqual(resolution, 65535)

    def test_build_file_header_returns_everything_correctly(self):
        infile = io.BytesIO(
            midi_file.build_file_header(0, 1, 2)
        )

        header_len, midi_format, track_ct, resolution = midi_file.parse_file_header(infile)

        self.assertEqual(infile.tell(), midi_file.DEFAULT_MIDI_HEADER_LEN)
        self.assertEqual(midi_format, 0)
        self.assertEqual(track_ct, 1)
        self.assertEqual(resolution, 2)

    def test_build_file_header_returns_midi_format_error(self):
        with self.assertRaises(TypeError):
            midi_file.build_file_header(5, 1, 1)

        self.assertTrue(self.log_handler.has_critical(re.compile('not a valid midi format'), channel='snail'))
