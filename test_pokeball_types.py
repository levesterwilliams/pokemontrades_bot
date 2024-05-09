import unittest
from pokeball_types import PokeballType

class TestPokeballTypes(unittest.TestCase):
    def test_validate_pokeball_valid01(self):
        self.assertTrue(PokeballType.validate_pokeball("love"))

    def test_validate_pokeball_valid02(self):
        self.assertTrue(PokeballType.validate_pokeball("dream"))

    def test_validate_pokeball_valid03(self):
        # Test with valid pokeball
        self.assertTrue(PokeballType.validate_pokeball("beast"))

    def test_validate_pokeball_valid04(self):
        self.assertTrue(PokeballType.validate_pokeball("moon"))

    def test_validate_pokeball_valid05(self):
        self.assertTrue(PokeballType.validate_pokeball("friend"))

    def test_validate_pokeball_valid06(self):
        self.assertTrue(PokeballType.validate_pokeball("heavy"))

    def test_validate_pokeball_valid07(self):
        self.assertTrue(PokeballType.validate_pokeball("lure"))

    def test_validate_pokeball_valid08(self):
        self.assertTrue(PokeballType.validate_pokeball("fast"))

    def test_validate_pokeball_valid09(self):
        self.assertTrue(PokeballType.validate_pokeball("level"))

    def test_validate_pokeball_valid10(self):
        self.assertTrue(PokeballType.validate_pokeball("safari"))

    def test_validate_pokeball_valid11(self):
        self.assertTrue(PokeballType.validate_pokeball("sport"))

    def test_validate_pokeball_valid12(self):
        self.assertTrue(PokeballType.validate_pokeball("pokeball"))

    def test_validate_pokeball_valid13(self):
        self.assertTrue(PokeballType.validate_pokeball("great"))

    def test_validate_pokeball_valid14(self):
        self.assertTrue(PokeballType.validate_pokeball("ultra"))

    def test_validate_pokeball_valid15(self):
        self.assertTrue(PokeballType.validate_pokeball("master"))

    def test_validate_pokeball_valid16(self):
        self.assertTrue(PokeballType.validate_pokeball("premier"))

    def test_validate_pokeball_valid17(self):
        self.assertTrue(PokeballType.validate_pokeball("repeat"))

    def test_validate_pokeball_valid18(self):
        self.assertTrue(PokeballType.validate_pokeball("timer"))

    def test_validate_pokeball_valid19(self):
        self.assertTrue(PokeballType.validate_pokeball("nest"))

    def test_validate_pokeball_valid20(self):
        self.assertTrue(PokeballType.validate_pokeball("net"))

    def test_validate_pokeball_valid21(self):
        self.assertTrue(PokeballType.validate_pokeball("dive"))

    def test_validate_pokeball_valid22(self):
        self.assertTrue(PokeballType.validate_pokeball("luxury"))

    def test_validate_pokeball_valid23(self):
        self.assertTrue(PokeballType.validate_pokeball("heal"))

    def test_validate_pokeball_valid24(self):
        self.assertTrue(PokeballType.validate_pokeball("quick"))

    def test_validate_pokeball_valid25(self):
        self.assertTrue(PokeballType.validate_pokeball("dusk"))

    def test_validate_pokeball_valid26(self):
        self.assertTrue(PokeballType.validate_pokeball("cherish"))

    def test_validate_pokeball_valid27(self):
        self.assertTrue(PokeballType.validate_pokeball("pokeball-h"))

    def test_validate_pokeball_valid28(self):
        self.assertTrue(PokeballType.validate_pokeball("great-h"))

    def test_validate_pokeball_valid29(self):
        self.assertTrue(PokeballType.validate_pokeball("ultra-h"))

    def test_validate_pokeball_valid30(self):
        self.assertTrue(PokeballType.validate_pokeball("feather"))

    def test_validate_pokeball_valid31(self):
        self.assertTrue(PokeballType.validate_pokeball("wing"))

    def test_validate_pokeball_valid32(self):
        self.assertTrue(PokeballType.validate_pokeball("jet"))

    def test_validate_pokeball_valid33(self):
        self.assertTrue(PokeballType.validate_pokeball("heavy-h"))

    def test_validate_pokeball_valid34(self):
        self.assertTrue(PokeballType.validate_pokeball("leaden"))

    def test_validate_pokeball_valid35(self):
        self.assertTrue(PokeballType.validate_pokeball("gigaton"))

    def test_validate_pokeball_valid36(self):
        self.assertTrue(PokeballType.validate_pokeball("origin"))

    def test_validate_pokeball_invalid(self):
        self.assertFalse(PokeballType.validate_pokeball("random"))


    def test_wrong_argument01(self):
        with self.assertRaises(TypeError) as context:
            PokeballType.validate_pokeball(1)
            self.assertEqual(str(context.exception), "Argument must be a "
                                                     "string")
    def test_wrong_argument02(self):
        with self.assertRaises(TypeError) as context:
            PokeballType.validate_pokeball(None)
            self.assertEqual(str(context.exception), "Argument must be a "
                                                     "string")

if __name__ == '__main__':
    unittest.main()