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

    def test_requested_pokemon_not_in_csv(self):
        sender_list = [{'Pokemon': 'Bulbasaur', 'pokeball': ['pokeball'], 'ability': ['overgrow']}]
        requested_list = [{'Pokemon': 'Pikachu', 'pokeball': ['pokeball'],
                           'ability': ['static']}]
        csv_data = {'pikachu': {'abilities': ['static'], 'pokeballs': ['pokeball']}}
        result = self.strategy.execute(sender_list, requested_list, csv_data)
        self.assertTrue(result)

    def test_requested_pokemon_mixed(self):
        sender_list = [{'Pokemon': 'Bulbasaur', 'pokeball': ['pokeball'], 'ability': ['overgrow']}]
        requested_list = [{'Pokemon': 'Pikachu', 'pokeball': ['pokeball'],
                           'ability': ['static']}]
        csv_data = {'pikachu': {'abilities': ['static'], 'pokeballs': ['pokeball']}}
        result = self.strategy.execute(sender_list, requested_list, csv_data)
        self.assertTrue(result, "Should return True if sender's Pokemon is "
                                 "not in CSV data")
        csv_data02 = {
            'pikachu': {'abilities': ['lightning rod'], 'pokeballs': [
                'pokeball']}}
        result = self.strategy.execute(sender_list, requested_list, csv_data02)
        self.assertFalse(result, "Should return False if sender's Pokemon is "
                                 "not in CSV data")

    def test_requested_pokemon_not_in_csv(self):
        sender_list = [{'Pokemon': 'Pikachu', 'pokeball': ['pokeball'], 'ability': ['static']}]
        requested_list = [{'Pokemon': 'Charmander', 'pokeball': ['pokeball'], 'ability': ['blaze']}]
        csv_data = {'pikachu': {'abilities': ['static'], 'pokeballs': ['pokeball']}}
        result = self.strategy.execute(sender_list, requested_list, csv_data)
        self.assertFalse(result, "Should return False if requested Pokemon is "
                                "not in CSV data")

    def test_matching_pokemon_in_csv(self):
        sender_list = [{'Pokemon': 'Pikachu', 'pokeball': ['pokeball'], 'ability': ['static']}]
        requested_list = [{'Pokemon': 'Bulbasaur', 'pokeball': ['pokeball'], 'ability': ['overgrow']}]
        csv_data = {
            'pikachu': {'abilities': ['static'], 'pokeballs': ['pokeball']},
            'bulbasaur': {'abilities': ['overgrow'], 'pokeballs': ['pokeball']}
        }
        result = self.strategy.execute(sender_list, requested_list, csv_data)
        self.assertFalse(result, "Should return False if all matching Pokemon are in CSV data")

    def test_non_matching_pokemon_attributes_in_csv(self):
        sender_list = [{'Pokemon': 'Pikachu', 'pokeball': ['greatball'], 'ability': ['lightning-rod']}]
        requested_list = [{'Pokemon': 'Bulbasaur', 'pokeball': ['ultraball'], 'ability': ['chlorophyll']}]
        csv_data = {
            'pikachu': {'abilities': ['static'], 'pokeballs': ['pokeball']},
            'bulbasaur': {'abilities': ['overgrow'], 'pokeballs': ['pokeball']}
        }
        result = self.strategy.execute(sender_list, requested_list, csv_data)
        self.assertTrue(result, "Should return True if attributes do not match in CSV data")

if __name__ == '__main__':
    unittest.main()
