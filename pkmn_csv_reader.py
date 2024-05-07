import pandas as pd
class PokemonCsvReader:
    def __init__(self):
        self._pokemons = {}

    def read_csv(self, filename):
        if filename is not type(str):
            raise TypeError("Argument must be a string.")

        data = pd.DataFrame()
        try:
            if filename.endswith('.csv'):
                data = pd.read_csv(filename)
            elif filename.endswith('.xlsx'):
                data = pd.read_excel(filename)
            else:
                raise ValueError("Unsupported file format")

            self.process_data(data)
        except (FileNotFoundError, PermissionError) as e:
            print(f"Error opening file: {e}")
        except pd.errors.EmptyDataError:
            print("Error: The file is empty")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        for _, row in data.iterrows():
            name = row['Name']
            abilities = row['Abilities'].split(
                ';')  # Assuming abilities are separated by semicolons
            pokeballs = row['Pokeballs'].split(';')  #

            if name not in self._pokemons:
                self._pokemons[name] = {
                    "Abilities": abilities,
                    "Pokeballs": pokeballs
                }
            else:
                self._pokemons[name]['Abilities'].extend(x for x in abilities
                                                         if x not in self._pokemons[name]['Abilities'])
                self._pokemons[name]['Pokeballs'].extend(x for x in pokeballs if x not in self._pokemons[name]['Pokeballs'])

    def get_pokemons(self):
        return self._pokemons