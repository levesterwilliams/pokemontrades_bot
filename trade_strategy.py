from typing import List, Dict, Any


class TradeStrategy:
    def _helper_execute(self, list: List[Dict[str, Any]], pkmn_csv_data:
    Dict[str, Any], flag: bool) -> bool:
        """
        The giveaway strategy is used to giveaway a pokemon not already marked in CSV
        , the recipient's list is ignored.

        Args:
            list (List[Dict[str, Any]): The list of Pokemon with
            associated values such as abilities, form, pokeball captured in,
            etc.
            pkmn_csv_data (Dict[str, Any]):  Data of Pokemon marked in a CSV

        Returns:
            bool: True if the request was successful, False otherwise.
        """

        if len(list) == 0 or len(pkmn_csv_data) == 0:
            return False
        print(list)
        print(f"flag is {flag}")
        for pokemon in list:
            name = pokemon["Pokemon"].lower()
            requested_pokeballs = pokemon.get("pokeball", [])
            requested_abilities = pokemon.get("ability", [])
            print(f"{name}")
            if name in pkmn_csv_data:
                pokeball_match = any(ball in pkmn_csv_data[name]['pokeballs']
                                     for ball in requested_pokeballs) if (
                    requested_pokeballs) else flag
                print (f"pokeball match is {pokeball_match}")
                abilities_match = any(
                    ability in pkmn_csv_data[name]['abilities'] for ability in
                    requested_abilities) if flag and requested_abilities else flag
                print(f"ability match is {abilities_match}")

                if flag and pokeball_match and abilities_match:
                   continue
                elif flag and (not pokeball_match or not abilities_match):
                    return True
                elif not flag and pokeball_match or abilities_match:
                    return True
                else:
                    continue
                #if (pokeball_match and abilities_match) or (not flag and not(
                       # pokeball_match and abilities_match)):
                    #continue
                #else:
                   # print(f"here 2 {flag}")
                    #return flag
            else:
                print(f"here 1 {flag}")
                return flag

        print(f"here 0 {flag}")
        return not flag

    def execute(self, sender_list: List[Dict[str, Any]],
                requested_list: List[Dict[str, Any]], pkmn_csv_data: Dict[str,
            Any]) -> bool:
        raise NotImplementedError(
            "This method should be overridden in subclasses.")

class LookingForTradeStrategy(TradeStrategy):
    """
    The looking for strategy is used to trade for a pokemon not already marked
    in CSV from the sender's list of pokemon not in the database.

    Args:
        sender_list (List[Dict[str, Any]): The list of Pokemon with
        associated values such as abilities, form, pokeball captured in,
        etc.
        requested_list (List[Dict[str, Any]): The list of Pokemon with
        associated values such as abilities, form, pokeball captured in,
            etc.
        pkmn_csv_data (Dict[str, Any]):  Data of Pokemon marked in a CSV

    Returns:
        bool: True if the request was successful, False otherwise.

    """

    def execute(self, sender_list: List[Dict[str, Any]],
                requested_list: List[Dict[str, Any]], pkmn_csv_data: Dict[str,
            Any]) -> bool:

        return (self._helper_execute(sender_list, pkmn_csv_data, True) and
                self._helper_execute(requested_list, pkmn_csv_data, False))





class GiveawayTradeStrategy(TradeStrategy):
    """
    The giveaway strategy is used to giveaway a pokemon not already marked in CSV
    , the recipient's list is ignored.

    Args:
        sender_list (List[Dict[str, Any]): The list of Pokemon with
        associated values such as abilities, form, pokeball captured in,
        etc.
        requested_list (List[Dict[str, Any]): The list of Pokemon with
        associated values such as abilities, form, pokeball captured in,
            etc. This will be ignored in this algorithm
        pkmn_csv_data (Dict[str, Any]):  Data of Pokemon marked in a CSV

    Returns:
        bool: True if the request was successful, False otherwise.

    """

    def execute(self, sender_list: List[Dict[str, Any]],
                requested_list: List[Dict[str, Any]], pkmn_csv_data: Dict[str,
            Any]) -> bool:

        return self._helper_execute(sender_list, pkmn_csv_data, True)