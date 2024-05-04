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

        Notes:
            If error occurs in opening the JSON file, the function will log an error message and the program will exit.
        """
        try:
            with open(json_file, 'r') as file:
                self._credentials = json.load(file)
                return self._credentials
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            logger.error(f"The JSON file contains invalid JSON: {e}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Error loading Reddit credentials: {e}")
            sys.exit(1)