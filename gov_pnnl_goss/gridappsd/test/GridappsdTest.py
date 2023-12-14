import unittest
from unittest import TestCase
from unittest.mock import Mock, patch
import inspect

class GridappsdTest(TestCase):

    def setUp(self):
        self.context = inspect.currentframe().f_back.f_globals.get('__name__', '')

    def test_gridappsd(self):
        self.assertIsNotNone(self.context)


if __name__ == '__main__':
    unittest.main()