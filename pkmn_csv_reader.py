import pandas as pd
import unicodedata
import re


class PokemonCsvReader:
    def __init__(self):
        self._pokemons = {}

    def read_csv(self, filename):
        if filename is not type(str):
            raise TypeError("Argument must be a string.")
        try:
            if filename.endswith('.csv'):
                data_frames = pd.read_csv(filename)
            elif filename.endswith('.xlsx'):
                data_frames = pd.read_excel(filename)
            else:
                raise ValueError("Unsupported file format")

            self.process_data(data_frames)
        except FileNotFoundError as e:
            raise FileNotFoundError("File not found.") from e
        except PermissionError as e:
            raise PermissionError("Permission denied.") from e
        except pd.errors.EmptyDataError:
            raise pd.errors.EmptyDataError("The file is empty.")
        except Exception as e:
            raise RuntimeError("Unexpected error: " + str(e))

    def normalize_and_clean(self, text):
        if not isinstance(text, str):
            raise TypeError("Argument must be a string.")

        normalized_text = unicodedata.normalize('NFKD', text)
        ascii_text = normalized_text.encode('ascii', 'ignore').decode('utf-8')
        lower_text = ascii_text.lower()
        cleaned_text = re.sub(r'[^\w\s]', '', lower_text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        return cleaned_text

    def find_column(self, df, column_name):
        if not isinstance(column_name, str):
            raise TypeError("Column name must be a string.")
        column_name = self.normalize_and_clean(column_name)
        for col in df.columns:
            if self.normalize_and_clean(col) == column_name:
                return col
        raise ValueError(f"Column not found: {column_name}")

    def process_data(self, data):
       if not isinstance(data, pd.DataFrame):
           raise TypeError("Expected pd.Dataframe. Actual type is : " + str(type(data)))

        for _, row in data.iterrows():
            poke_col_header = self.find_column(data, "Pokemon")
            ability_col_header = self.find_column(data, "Ability")
            balls_col_list = data.columns[data.columns.get_loc(
                ability_col_header) + 1:]
            if not isinstance(poke_col_header, str) or not isinstance(ability_col_header,
                                                               str):
                raise TypeError("String expected for columns")
            poke_name = row[poke_col_header]
            abilities = row[ability_col_header].split(',') if pd.notna(row[ability_col_header]) else []
            abilities = [ability.strip() for ability in abilities]

            pokeballs = [pb for pb in balls_col_list if
                         pd.notna(row[pb]) and row[pb].strip() != '']

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
                self._pokemons[poke_name]['Abilities'] = updated_abilities
                self._pokemons[poke_name]['Pokeballs'] = updated_pokeballs


    def get_pokemons(self):
        return self._pokemons

