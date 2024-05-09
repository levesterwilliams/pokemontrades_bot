import unittest
from unittest.mock import patch
import pandas as pd
from pkmn_csv_reader import PokemonCsvReader
from pathlib import Path


def create_test_data(headers, data):
    return pd.DataFrame(data, columns=headers)


class TestFileReader(unittest.TestCase):
    """
    Test the PokemonCsvReader
    """

    def setUp(self):
        self._reader = PokemonCsvReader()

    @patch('pandas.read_csv')
    def test_read_csv_file(self, mock_read_file):
        mock_read_file.return_value = pd.DataFrame(
            {'Pokemon': ['Pikachu'], 'Ability': ['Static']})
        self._reader.read_file('test.csv')
        self.assertIn('pikachu', self._reader.get_pokemons())
        self.assertEqual(self._reader.get_pokemons()['pikachu']['abilities'],
                         ['static'])
        print(self._reader.get_pokemons())

    @patch('pandas.read_excel')
    def test_read_excel_file(self, mock_read_excel):
        mock_read_excel.return_value = pd.DataFrame(
            {'Pokemon': ['Bulbasaur'], 'Ability': ['Overgrow'], 'master': [
                "x"]})
        self._reader.read_file('test.xlsx')
        dict = self._reader.get_pokemons()
        self.assertIn('bulbasaur', dict)
        pokeball = dict["bulbasaur"]['pokeballs'][0]
        self.assertEqual("master", pokeball)
        self.assertEqual(dict['bulbasaur']['abilities'],
                         ['overgrow'])

    def test_invalid_file_type(self):
        with self.assertRaises(RuntimeError) as context:
            self._reader.read_file('test.txt')
            self.assertEqual(str(context.exception), "Unexpected error: " +
                             str(context.excpetion))

    @patch('pandas.read_csv', side_effect=FileNotFoundError)
    def test_file_not_found(self, mock_read_csv):
        with self.assertRaises(FileNotFoundError) as context:
            self._reader.read_file('missing.csv')
        self.assertEqual(str(context.exception), "File not found.")

    @patch('pandas.read_csv', side_effect=PermissionError)
    def test_permission_error(self, mock_read_csv):
        with self.assertRaises(PermissionError) as context:
            self._reader.read_file('protected.csv')
        self.assertEqual(str(context.exception), "Permission denied.")

    @patch('pandas.read_csv', side_effect=pd.errors.EmptyDataError)
    def test_empty_file(self, mock_read_csv):
        with self.assertRaises(pd.errors.EmptyDataError) as context:
            self._reader.read_file('empty.csv')
        self.assertEqual(str(context.exception), "The file is empty.")

    def test_non_string_argument(self):
        with self.assertRaises(TypeError) as context:
            self._reader.read_file(123)
        self.assertEqual(str(context.exception), "Argument must be a string.")

    @patch('pandas.read_csv', side_effect=Exception("Some error"))
    def test_unexpected_error(self, mock_read_csv):
        with self.assertRaises(RuntimeError) as context:
            self._reader.read_file('unexpected.csv')
        self.assertTrue(
            "Unexpected error: Some error" in str(context.exception))

    @patch('pandas.read_csv')
    def test_empty_csv(self, mock_read_file):
        mock_read_file.return_value = create_test_data([],
                                                       [])
        self._reader.read_file('empty.csv')
        self.assertEqual(self._reader.get_pokemons(), {}, "Should handle empty "
                                                          "CSV without errors.")

    @patch('pandas.read_csv')
    def test_missing_pokemon_header(self, mock_read_file):
        mock_read_file.return_value = create_test_data(['Ability'],
                                                       [{
                                                           'Ability': 'Levitate'}])
        with self.assertRaises(RuntimeError):
            self._reader.read_file("missing_pokemon.csv")

    @patch('pandas.read_csv')
    def test_missing_ability_header(self, mock_read_file):
        mock_read_file.return_value = create_test_data(['Pokemon'],
                                                       [{'Pokemon': 'Pikachu'}])
        with self.assertRaises(RuntimeError):
            self._reader.read_file('missing_ability.csv')

    def test_normal_input(self):
        input_text = "Café Pokémon"
        expected_output = "cafe pokemon"
        result = self._reader.normalize_and_clean(input_text)
        self.assertEqual(result, expected_output)

    def test_non_string_argument(self):
        with self.assertRaises(TypeError) as context:
            self._reader.normalize_and_clean(123)
        self.assertEqual(str(context.exception), "Argument must be a string.")

    def test_empty_string(self):
        input_text = ""
        expected_output = ""
        result = self._reader.normalize_and_clean(input_text)
        self.assertEqual(result, expected_output)

    def test_whitespace_management(self):
        input_text = "   Hello    Pokémon  "
        expected_output = "hello pokemon"
        result = self._reader.normalize_and_clean(input_text)
        self.assertEqual(result, expected_output)

    def test_special_characters(self):
        input_text = "Ráichu, Búlbasaur & Mew!"
        expected_output = "raichu bulbasaur mew"
        result = self._reader.normalize_and_clean(input_text)
        self.assertEqual(result, expected_output)

    def test_accented_characters(self):
        input_text = "Pokémon é cáfé"
        expected_output = "pokemon e cafe"
        result = self._reader.normalize_and_clean(input_text)
        self.assertEqual(result, expected_output)

    def test_mixed_case_and_punctuation(self):
        input_text = "PokéMon, 123 - @BulbAsaur!"
        expected_output = "pokemon 123 bulbasaur"
        result = self._reader.normalize_and_clean(input_text)
        self.assertEqual(result, expected_output)

    @patch('pandas.read_csv')
    def test_special_characters01(self, mock_read_file):
        mock_read_file.return_value = create_test_data(
            ['Pokémon', 'Abîlity'],
            [{'Pokémon': 'Pikáchu', 'Abîlity': 'Státic'}]
        )
        self._reader.read_file('special_characters.csv')
        expected = {'pikachu': {'abilities': ['static'], 'pokeballs': []}}
        self.assertEqual(self._reader.get_pokemons(), expected,
                         "Should correctly handle special characters.")

    @patch('pandas.read_csv')
    def test_find_column_normal_case(self, mock_read_file):
        mock_read_file.return_value = create_test_data(
            ['Pokémon', 'Abîlity'],
            [{'Pokémon': 'Pikáchu', 'Abîlity': 'Státic'}]
        )
        column_name = self._reader.find_column(mock_read_file.return_value, 'Pokemon')
        self.assertEqual(column_name, 'Pokémon')

    @patch('pandas.read_csv')
    def test_find_column_case_insensitivity(self, mock_read_file):
        mock_read_file.return_value = create_test_data(
            ['Pokémon', 'ability', 'poke'],
            [{'Pokémon': 'Pikáchu', 'ability': 'Státic', 'poke': 'x'},
             {'Pokémon': 'Gengar', 'ability': 'Levitate', 'poke': 'x'}])

        column_name = self._reader.find_column(mock_read_file.return_value, 'ability')
        self.assertEqual(column_name, 'ability')
    @patch('pandas.read_csv')
    def test_find_column_special_characters(self, mock_read_file):
        mock_read_file.return_value = create_test_data(
            ['Pokémon', 'ability', 'specîal-name'],
            [{'Pokémon': 'Pikáchu', 'ability': 'Státic', 'specîal-name': 'x'},
             {'Pokémon': 'Gengar', 'ability': 'Levitate', 'specîal-name': 'x'}])

        column_name = self._reader.find_column(mock_read_file.return_value,
                                               'specîal-name')
        self.assertEqual(column_name, 'specîal-name')

    def test_find_column_not_found(self):
        df = pd.DataFrame()
        with self.assertRaises(ValueError) as context:
            self._reader.find_column(df, 'NonExistentColumn')
        self.assertEqual(str(context.exception),
                         "Column not found: nonexistentcolumn")

    def test_find_column_non_string_name(self):
        df = pd.DataFrame()
        with self.assertRaises(TypeError) as context:
            self._reader.find_column(df, 123)
        self.assertEqual(str(context.exception),
                         "Column name must be a string.")
    @patch('pandas.read_csv')
    def test_find_column_with_normalization(self, mock_read_file):
        mock_read_file.return_value = create_test_data(
            ['Pokémon', 'ability', 'Specîal-name'],
            [{'Pokémon': 'Pikáchu', 'ability': 'Státic', 'Specîal-name': 'x'},
             {'Pokémon': 'Gengar', 'ability': 'Levitate', 'Specîal-name': 'x'}])
        column_name = self._reader.find_column(mock_read_file.return_value,
                                               'Specîal-name')
        self.assertEqual(column_name, 'Specîal-name')

    def test_special_characters02(self):
        project_root = Path.cwd()
        csv_path = project_root / 'files' / 'pokemon-list01.csv'
        path_str = str(csv_path)
        self._reader.read_file(path_str)
        expected = {'sprigatito': {'abilities': [], 'pokeballs': [
            'premier']}, 'quaxly': {'abilities': [], 'pokeballs': [
            'premier']}, 'fuecoco': {'abilities': [], 'pokeballs': [
            'premier']}, 'cerulege': {'abilities': [], 'pokeballs': []},
                    'iron boulder': {'abilities': [], 'pokeballs': []},
                    'iron crown': {'abilities': [], 'pokeballs': []},
                    'pansage': {'abilities': [], 'pokeballs': ['master']},
                    'pansear': {'abilities': [], 'pokeballs': []},
                    'simisage': {'abilities': [], 'pokeballs': []}}
        self.assertEqual(self._reader.get_pokemons(), expected)


if __name__ == '__main__':
    unittest.main()
