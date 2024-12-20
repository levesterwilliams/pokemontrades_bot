# pkmn_csv_reader.py
#
# Levester Williams
# 25 April 2024
#
# Platform info:
# - python 3.12.0
#

import pandas as pd
import unicodedata
import re
from pathlib import Path
from pokeball_types import validate_pokeball

class PokemonCsvReader:
    """
    Class to read the csv file or Excel file containing registered Pokemon data
    about abilities and pokeballs captured in. The class returns a dict of
    Pokemons that cantains a dict with "abilities" key with list of its
    abilities as values and dict with "pokeballs" key with a list of pokeball
    types as values.

    """
    def __init__(self):
        self._pokemons = {}

    def read_file(self, filename: str) -> None:
        """
        Reads the csv file.

        Args:
            filename (str): The name of the csv file.

        Returns:
            None

        Raise:
            ValueError if the filename is unsupported or the filename isn't
            a valid csv file'

            FileNotFoundError if the filename does not exist

            PermissionError if the filename is locked

            pd.errors.EmptyDataError if the file is empty; and RuntimeError if
            the file runs into other issues.
        """
        try:
            if filename.endswith('.csv'):
                data_frames = pd.read_csv(filename)
            elif filename.endswith('.xlsx'):
                data_frames = pd.read_excel(filename)
            else:
                raise ValueError("Unsupported file format")
                # ultimately, will be pinged again as RuntimeError

            self.process_data(data_frames)
        except FileNotFoundError as e:
            raise FileNotFoundError("File not found.") from e
        except PermissionError as e:
            raise PermissionError("Permission denied.") from e
        except pd.errors.EmptyDataError:
            raise pd.errors.EmptyDataError("The file is empty.")
        except Exception as e:
            raise RuntimeError("Unexpected error: " + str(e))

    def normalize_and_clean(self, text: str) -> str:
        """
        Normalize and clean the text to remove punctuation and whitespace.

        Args:
            text (str): The text to normalize and clean.

        Returns:
            str: The normalized text.
        """
        normalized_text = unicodedata.normalize('NFKD', text)
        ascii_text = normalized_text.encode('ascii', 'ignore').decode('utf-8')
        lower_text = ascii_text.lower()
        cleaned_text = re.sub(r'[^\w\s]', '', lower_text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        cleaned_text = cleaned_text.replace("á", "a")
        cleaned_text = cleaned_text.replace("é", "e")
        cleaned_text = cleaned_text.replace("î", "i")
        return cleaned_text

    def find_column(self, df: pd.DataFrame, column_name: str) -> str:
        """
        Find the column.

        Args:
            df (pandas.DataFrame): Dataframe to find the column
            column_name (str): Name of the column to find

        Returns:
            (str): Column

        Raises:
            ValueError: If the column is not found.
        """
        column_name = self.normalize_and_clean(column_name)
        for col in df.columns:
            if self.normalize_and_clean(col) == column_name:
                return col
        raise ValueError(f"Column not found: {column_name}")

    def process_data(self, data: pd.DataFrame) -> None:
        """
        Process the dataframe from a pokemon csv file and store the parsed data
        in inside _pokemon, a dict.

        Args:
            data (list): List of pandas dataframes

        Returns:
            None
        """
        for _, row in data.iterrows():
            poke_col_header = self.find_column(data, "Pokemon")
            ability_col_header = self.find_column(data, "Ability")
            balls_col_list = data.columns[data.columns.get_loc(ability_col_header) + 1:]

            if not isinstance(poke_col_header, str) or not isinstance(ability_col_header,
                                                               str):
                raise TypeError("String expected for columns")
            poke_name = row[poke_col_header]
            poke_name = self.normalize_and_clean(poke_name)
            abilities = row[ability_col_header].split(',') if pd.notna(row[ability_col_header]) else []
            abilities = [self.normalize_and_clean(ability) for ability in
                         abilities]
            pokeballs = [self.normalize_and_clean(pb) for pb in
                         balls_col_list if
                         pd.notna(row[pb]) and row[pb].strip() != '' and
                         validate_pokeball(self.normalize_and_clean(pb))]

            if poke_name not in self._pokemons:
                self._pokemons[poke_name] = {
                    "abilities": abilities,
                    "pokeballs": pokeballs
                }
            else:
                current_abilities = set(self._pokemons[poke_name]["abilities"])
                current_pokeballs = set(self._pokemons[poke_name]["pokeballs"])
                updated_abilities = list(current_abilities.union(abilities))
                updated_pokeballs = list(current_pokeballs.union(pokeballs))
                self._pokemons[poke_name]['abilities'] = updated_abilities
                self._pokemons[poke_name]['pokeballs'] = updated_pokeballs


    def get_pokemons(self):
        """
        Return a nested dict of Pokemons where each key is a specific Pokemon
        name and its value is a dict that contains the Pokemon's "abilities"
        as a key and a list of its abilities as its values and another key
        "pokeballs" with a list of pokeball types as values

        Args:
            None

        Returns:
            _pokemons: A dict of Pokemons that contains a dict with "abilities"
            as the key and its list of abilities as values and dict
            "pokeballs" with a list of pokeball types as values
        """
        return self._pokemons

