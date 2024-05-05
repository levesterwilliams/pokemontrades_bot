import unittest
from unittest.mock import mock_open, patch
import json
from JSON_freader import JSONfreader

class TestJSONfreader(unittest.TestCase):
    """
        Test Suite for JSONfreader class.

        This test class is designed to validate the functionality of the JSONfreader class,
        which is responsible for loading credentials from a JSON file. The tests ensure that
        the JSONfreader handles various scenarios correctly, including successful file loading,
        handling of file not found errors, invalid JSON data, and other exceptions.

        Attributes:
            reader (JSONfreader): An instance of the JSONfreader class used for testing.
    """
    def setUp(self):
        self.reader = JSONfreader()

    @patch("builtins.open", new_callable=mock_open, read_data='{"user": '
                                                              '"admin", "password": "1234"}')
    def test_load_json_file_success(self, mock_file):
        result = self.reader.load_json_file("credentials.json")
        self.assertEqual(result, {"user": "admin", "password": "1234"})

    @patch("builtins.open", mock_open())
    @patch("json.load", side_effect=FileNotFoundError("File not found"))
    def test_load_json_file_not_found(self, mock_json_load):
        with self.assertRaises(SystemExit) as cm:
            self.reader.load_json_file("nonexistent.json")
        self.assertEqual(cm.exception.code, 1)

    @patch("builtins.open", mock_open())
    @patch("json.load", side_effect=json.JSONDecodeError("Expecting value", "line 1 column 1 (char 0)", 0))
    def test_load_json_file_invalid_json(self, mock_json_load):
        with self.assertRaises(SystemExit) as cm:
            self.reader.load_json_file("invalid.json")
        self.assertEqual(cm.exception.code, 1)

    @patch("builtins.open", mock_open())
    @patch("json.load", side_effect=Exception("Unexpected error"))
    def test_load_json_file_unexpected_error(self, mock_json_load):
        with self.assertRaises(SystemExit) as cm:
            self.reader.load_json_file("error.json")
        self.assertEqual(cm.exception.code, 1)

if __name__ == "__main__":
    unittest.main()
