# jsonf_reader.py
#
# Levester Williams
# 31 July 2024
#
# Platform info:
# - python 3.12.0
#

import json
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)

class JSONfreader:
    """This class reads a json file and return credentials to client/caller.

        Attributes:
        -----------
        _credentials : dict
            A dictionary containing the credentials.

        Methods
        -------
        load_json_file():
            Loads credentials from an external JSON file.
    """
    def __init__(self):
        """Initializer for JSONfreader class."""
        self._credentials = None

    def load_json_file(self, json_file: str) -> dict:
        """
        Loads Reddit credentials from an external JSON file.

        Args:
            json_file (str): Path to the JSON file

        Returns:
            dict: Dictionary containing the loaded credentials, or None if an
            error occurs.

        Raises:
            RuntimeError: A runtime error is raised any errors occur in loading
            the JSON file.

        Notes:
            If error occurs in opening the JSON file, the function will log
            an error message and raise a runtime error exception for
            client/caller to handle.
        """
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
