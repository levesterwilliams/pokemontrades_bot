import unittest
from trade_strategy import LookingForTradeStrategy

class TestLookingForTradeStrategy(unittest.TestCase):

    def setUp(self):
        self.strategy = LookingForTradeStrategy()

    def test_empty_sender_list(self):
        sender_list = [{'Pokemon': 'Pikachu', 'pokeball': ['pokeball'], 'ability': ['static']}]
        requested_list = []
        csv_data = {'pikachu': {'abilities': ['static'], 'pokeballs': ['pokeball']}}
        result = self.strategy.execute(sender_list, requested_list, csv_data)
        self.assertFalse(result)

    def test_empty_csv_data(self):
        sender_list = [{'Pokemon': 'Pikachu', 'pokeball': ['pokeball'], 'ability': ['static']}]
        requested_list = [{'Pokemon': 'Bulbasaur', 'pokeball': ['pokeball'], 'ability': ['overgrow']}]
        csv_data = {}
        result = self.strategy.execute(sender_list, requested_list, csv_data)
        self.assertFalse(result)

    def test_requested_pokemon_yes_trade_csv(self):
        sender_list = [{'Pokemon': 'Bulbasaur', 'pokeball': ['pokeball'], 'ability': ['overgrow']}]
        requested_list = [{'Pokemon': 'Pikachu', 'pokeball': ['pokeball'],
                           'ability': ['static']}]
        csv_data = {'pikachu': {'abilities': ['static'], 'pokeballs': ['pokeball']}}
        result = self.strategy.execute(sender_list, requested_list, csv_data)
        self.assertTrue(result)

    def test_requested_pokemon_no_trade_csv(self):
        sender_list = [{'Pokemon': 'Bulbasaur', 'pokeball': ['pokeball'],
                        'ability': ['overgrow']}]
        requested_list = [{'Pokemon': 'Pikachu', 'pokeball': ['pokeball'],
                           'ability': ['static']}]
        csv_data = {
            'pichu': {'abilities': ['static'], 'pokeballs': ['pokeball']}}
        result = self.strategy.execute(sender_list, requested_list, csv_data)
        self.assertFalse(result)

    def test_requested_pokemon_mixed(self):
        sender_list = [{'Pokemon': 'Bulbasaur', 'pokeball': ['pokeball'], 'ability': ['overgrow']}]
        requested_list = [{'Pokemon': 'Pikachu', 'pokeball': ['pokeball'],
                           'ability': ['static']}]
        csv_data = {'pikachu': {'abilities': ['static'], 'pokeballs': ['pokeball']}}
        result = self.strategy.execute(sender_list, requested_list, csv_data)
        self.assertTrue(result, "Should return True if sender's Pokemon is "
                                 "not in CSV data")
        csv_data02 = {
            'pichu': {'abilities': ['lightning rod'], 'pokeballs': [
                'pokeball']}}
        result = self.strategy.execute(sender_list, requested_list, csv_data02)
        self.assertFalse(result)

    def test_requested_pokemon_multiple_requests_no01(self):
        sender_list = [{'Pokemon': 'Pikachu', 'pokeball': ['pokeball'],
                        'ability': ['static']}]
        requested_list = [{'Pokemon': 'Charmander', 'pokeball': ['pokeball'],
                           'ability': ['blaze']}, {'Pokemon': 'pikachu',
                                                   'pokeball': ['pokeball'],
                                                   'ability': ['static']}]
        csv_data = {'pikachu': {'abilities': ['static'], 'pokeballs': ['pokeball']}}
        result = self.strategy.execute(sender_list, requested_list, csv_data)
        self.assertFalse(result)

    def test_requested_pokemon_multiple_requests_no02(self):
        sender_list = [{'Pokemon': 'Pikachu', 'pokeball': ['pokeball'],
                        'ability': ['static']}, {'Pokemon': 'Stakataka',
                                                  'pokeball': ['master'],
                        'ability': []}]
        requested_list = [{'Pokemon': 'Charmander', 'pokeball': ['pokeball'],
                           'ability': ['blaze']}, {'Pokemon': 'pikachu',
                                                   'pokeball': ['pokeball'],
                                                   'ability': ['static']}]
        csv_data = {'pikachu': {'abilities': ['lightning rod'], 'pokeballs': [
            'heavy']}}
        result = self.strategy.execute(sender_list, requested_list, csv_data)
        self.assertFalse(result)


    def test_matching_pokemon_in_csv(self):
        sender_list = [{'Pokemon': 'Pikachu', 'pokeball': ['pokeball'], 'ability': ['static']}]
        requested_list = [{'Pokemon': 'Bulbasaur', 'pokeball': ['pokeball'], 'ability': ['overgrow']}]
        csv_data = {
            'pikachu': {'abilities': ['static'], 'pokeballs': ['pokeball']},
            'bulbasaur': {'abilities': ['overgrow'], 'pokeballs': ['pokeball']}
        }
        result = self.strategy.execute(sender_list, requested_list, csv_data)
        self.assertFalse(result)

    def test_non_matching_pokemon_attributes_in_csv(self):
        sender_list = [{'Pokemon': 'Pikachu', 'pokeball': ['great'], 'ability': ['lightning-rod']}]
        requested_list = [{'Pokemon': 'Bulbasaur', 'pokeball': ['ultraball'], 'ability': ['chlorophyll']}]
        csv_data = {
            'pikachu': {'abilities': ['static'], 'pokeballs': ['pokeball']},
            'bulbasaur': {'abilities': ['overgrow'], 'pokeballs': ['pokeball']}
        }
        result = self.strategy.execute(sender_list, requested_list, csv_data)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
