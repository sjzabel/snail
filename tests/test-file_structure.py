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
