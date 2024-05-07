import unittest
from GPT35TurboClient import GPT35TurboClient
from JSON_freader import JSONfreader
import openai

class TestGPT35TurboClient(unittest.TestCase):
    """
    Test Suite for the GPT35TurboClient class.

    This class tests the GPT35TurboClient to ensure it correctly initializes
    with valid input parameters and handles various input types gracefully,
    preventing and reporting type errors. It also tests the functionality of
    generating specific JSON strings based on the input to validate both the
    successful generation of strings and proper handling of erroneous inputs.
    """
    def test_initialization_successful(self):
        self.client = GPT35TurboClient("key", "model")
        self.assertEqual(self.client._finetuned_model, "model")

    def test_init_type_error01(self):
        # Test with non-string for _secret_key
        with self.assertRaises(TypeError):
            GPT35TurboClient(123, "valid_model_name")

    def test_init_type_error02(self):
        # Test with non-string for _finetuned_model
        with self.assertRaises(TypeError):
            GPT35TurboClient("key", 5)

    def test_init_type_error03(self):
        # Test with non-string for None
        with self.assertRaises(TypeError):
            GPT35TurboClient(None, None)

    def test_generate_jsonstring_successful01(self):
        reader = JSONfreader()
        cred = reader.load_json_file('ftGPTturbo_pkmn_cred.json')
        client = GPT35TurboClient(cred['secret_key'], cred['model_name'])
        self.assertEqual("{ \"Sender's Pokemon\" :  [] , \"Requested Pokemon\" : [] , \"version\" : \"SWSH\" , \"action\" : \"closed\" }",
                         client.generate_jsonstring("Help me evolve my "
                                                    "spritzee\nSWSH (Closed)\n\nI have sachet just need TB"))

    def test_generate_jsonstring_successful02(self):
        reader = JSONfreader()
        cred = reader.load_json_file('ftGPTturbo_pkmn_cred.json')
        client = GPT35TurboClient(cred['secret_key'], cred['model_name'])
        self.assertEqual("{ \"Sender's Pokemon\" :  [] , \"Requested Pokemon\" : [ { \"Pokemon\" : \"Cranidos\" , \"IV\" : [] , \"nature\" : [] , \"gender\" : [] , \"ability\" : [] , \"hidden ability\" : [] , \"language\" : [] , \"form\" : [] , \"special\" : [] , \"pokeball\" : [] , \"shiny\" : false } ] , \"version\" : \"PLA\" , \"action\" : \"trade\" }",
                         client.generate_jsonstring("LF: Cranidos to complete Pokédex\nPLA"))

    def test_generate_jsonstring_error01(self):
        reader = JSONfreader()
        cred = reader.load_json_file('ftGPTturbo_pkmn_cred.json')
        client = GPT35TurboClient(cred['secret_key'], cred['model_name'])
        with self.assertRaises(TypeError):
             client.generate_jsonstring(None)

    def test_generate_jsonstring_error02(self):
        reader = JSONfreader()
        cred = reader.load_json_file('ftGPTturbo_pkmn_cred.json')
        client = GPT35TurboClient(cred['secret_key'], cred['model_name'])
        with self.assertRaises(TypeError):
             client.generate_jsonstring(1)


if __name__ == '__main__':
    unittest.main()
