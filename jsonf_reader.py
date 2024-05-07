import json
import sys
import logging

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)

class JSONfreader:
    def __init__(self):
        """Initializer for JSONfreader class."""
        self._credentials = None

    def load_json_file(self, json_file):
        """
        Loads Reddit credentials from an external JSON file.

        Args:
            json_file (str): Path to the JSON file

        Returns:
            dict: Dictionary containing the loaded credentials, or None if an error occurs.

        Raises:
            TypeError: A type error is raised if filename is not a string.
            RuntimeError: A runtime error is raised any errors occur.

        Notes:
            If error occurs in opening the JSON file, the function will log
            an error message and raise a runtime error exception for
            client/caller to handle.
        """
        if not isinstance(json_file, str):
            raise TypeError("Argument must be a string")

        try:
            with open(json_file, 'r') as file:
                self._credentials = json.load(file)
                return self._credentials
        except FileNotFoundError as e:
            logger.error(f"File not found{e}")
            raise RuntimeError("Failed to load credentials due to missing file.") from e
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON::{e}")
            raise RuntimeError("The JSON file contains invalid JSON") from e
        except Exception as e:
            logger.error(f"Error loading Reddit credentials::{e}")
            raise RuntimeError("Error in loading Reddit credentials") from e
