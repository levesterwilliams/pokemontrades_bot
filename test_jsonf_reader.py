# test_jsonf_reader.py
#
# Levester Williams
# 31 July 2024
#
# Platform info:
# - python 3.12.0
#

import unittest
from unittest.mock import mock_open, patch
import json
from jsonf_reader import JSONfreader

class TestJSONfreader(unittest.TestCase):
    """
    Test Suite for JSONfreader class.

    This test class is designed to validate the functionality of the
    JSONfreader class, which is responsible for loading credentials from
    a JSON file. The tests ensure that the JSONfreader handles various
    scenarios correctly, including successful file loading, handling of
    file not found errors, invalid JSON data, and other exceptions.
    """
    def setUp(self):
        self.reader = JSONfreader()

    def test_load_json_file_successful(self):
        with patch("builtins.open", new_callable=mock_open,
                   read_data='{"user": "admin", "password": "1234"}'):
            result = self.reader.load_json_file("credentials.json")
            self.assertEqual(result, {"user": "admin", "password": "1234"})

    def test_load_json_file_not_found01(self):
        with patch("builtins.open", mock_open()) as mocked_open:
            mocked_open.side_effect = FileNotFoundError

            with self.assertRaises(RuntimeError) as context:
                self.reader.load_json_file("nonexistent.json")
            self.assertEqual(str(context.exception), "Failed to load "
                                                     "credentials due to missing"
                                                     " file.")

    def test_load_json_file_not_found02(self):
        with patch("builtins.open", mock_open()) as mocked_open:
            mocked_open.side_effect = FileNotFoundError

            with self.assertRaises(RuntimeError) as context:
                self.reader.load_json_file("")
            self.assertEqual(str(context.exception),
                             "Failed to load credentials due to missing file.")

    def test_load_json_file_invalid_json(self):
        with patch("builtins.open", mock_open()) as mocked_open:
            mocked_open.side_effect = json.JSONDecodeError("Expecting "
                                                            "value", "line 1 column 1 (char 0)", 0)

            with self.assertRaises(RuntimeError) as context:
                 self.reader.load_json_file("invalid.json")
            self.assertEqual(str(context.exception), "The JSON file contains invalid JSON")


    def test_load_json_file_unexpected_error(self):
        with patch("builtins.open", mock_open()) as mocked_open:
            mocked_open.side_effect = Exception

            with self.assertRaises(RuntimeError) as context:
                self.reader.load_json_file("error.json")
            self.assertEqual(str(context.exception), "Error in loading Reddit credentials")

if __name__ == "__main__":
    unittest.main()
