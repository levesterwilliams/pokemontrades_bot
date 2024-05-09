import unittest
from trade_strategy import GiveawayTradeStrategy


class TestGiveawayStrategy(unittest.TestCase):

    def setUp(self):
        self.strategy = GiveawayTradeStrategy()

    def test_empty_sender_list(self):
        sender_list = []
        requested_list = []
        csv_data = {
            'pikachu': {'abilities': ['static'], 'pokeballs': ['pokeball']}}
        result = self.strategy.execute(sender_list, requested_list, csv_data)
        self.assertFalse(result)

    def test_empty_csv_data(self):
        sender_list = [{'Pokemon': 'Pikachu', 'pokeball': ['pokeball'],
                        'ability': ['static']}]
        requested_list = []
        csv_data = {}
        result = self.strategy.execute(sender_list, requested_list, csv_data)
        self.assertFalse(result)

    def test_pokemon_not_in_csv(self):
        sender_list = [{'Pokemon': 'Bulbasaur', 'pokeball': ['pokeball'],
                        'ability': ['overgrow']}]
        requested_list = []
        csv_data = {
            'pikachu': {'abilities': ['static'], 'pokeballs': ['pokeball']}}
        result = self.strategy.execute(sender_list, requested_list, csv_data)
        self.assertTrue(result)

    def test_pokemon_in_csv_with_matching_attributes(self):
        sender_list = [{'Pokemon': 'Pikachu', 'pokeball': ['pokeball'],
                        'ability': ['static']}]
        requested_list = []
        csv_data = {
            'pikachu': {'abilities': ['static'], 'pokeballs': ['pokeball']}}
        result = self.strategy.execute(sender_list, requested_list, csv_data)
        self.assertFalse(result)

    def test_pokemon_in_csv_with_non_matching_pokeballs(self):
        sender_list = [{'Pokemon': 'Pikachu', 'pokeball': ['great'],
                        'ability': ['static']}]
        requested_list = []
        csv_data = {
            'pikachu': {'abilities': ['static'], 'pokeballs': ['pokeball']}}
        result = self.strategy.execute(sender_list, requested_list, csv_data)
        self.assertTrue(result)

    def test_pokemon_in_csv_with_non_matching_abilities(self):
        sender_list = [{'Pokemon': 'Pikachu', 'pokeball': ['pokeball'],
                        'ability': ['lightning-rod']}]
        requested_list = []
        csv_data = {
            'pikachu': {'abilities': ['static'], 'pokeballs': ['pokeball']}}
        result = self.strategy.execute(sender_list, requested_list, csv_data)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()