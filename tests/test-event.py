from snail import event
from unittest.mock import MagicMock
import io
import logbook
import re
import struct
import unittest


class TestEvent(unittest.TestCase):
    def setUp(self):
        self.log_handler = logbook.TestHandler()
        self.log_handler.push_thread()
        self.stderrhndlr = logbook.StderrHandler(level='DEBUG', bubble=True)
        # add with self.stderrhndlr.applicationbound():
        # to see logging

        self.event_start = [
        ]

    def tearDown(self):
        self.log_handler.pop_thread()

    def test_parse_tick(self):
        pass

    def test_parse_event_code(self):
        pass

    def test_parse_sysex_event(self):
        pass

    def test_parse_meta_event(self):
        pass

    def test_parse_continuation_event(self):
        pass

    def test_event_channel(self):
        pass
