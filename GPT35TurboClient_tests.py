import unittest
from GPT35TurboClient import GPT35TurboClient
from JSON_freader import JSONfreader
import openai

class MyTestCase(unittest.TestCase):

    def test_initialization_variables01(self):
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
        self.assertEqual("{ \"Sender's Pokemon\" :  [ { \"Pokemon\" : \"Pansage\" , \"IV\" : [] , \"nature\" : [] , \"gender\" : [] , \"ability\" : [] , \"hidden ability\" : [] , \"language\" : [] , \"form\" : [] , \"special\" : [] , \"pokeball\" :[] , \"shiny\" : false } , { \"Pokemon\" : \"Pansear\" , \"IV\" : [] , \"nature\" : [] , \"gender\" : [] , \"ability\" : [] , \"hidden ability\" : [] , \"language\" : [] , \"form\" : [] , \"special\" : [] , \"pokeball\" :[] , \"shiny\" : false } ] , \"Requested Pokemon\" : [ { \"Pokemon\" : \"Simisage\" , \"IV\" : [] , \"nature\" : [] , \"gender\" : [] , \"ability\" : [] , \"hidden ability\" : [] , \"language\" : [] , \"form\" : [] , \"special\" : [] , \"pokeball\" : [] , \"shiny\" : false } ] , \"version\" : \"Home\" , \"action\" : \"trade\" }",
                         client.generate_jsonstring("LF: Simisage FT: Pansage/ Pansear\nHome\n"))

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
