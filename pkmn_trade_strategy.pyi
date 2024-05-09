from typing import List, Dict, Any

class TradeStrategy:
    """
    The interface for the strategy design pattern where execute must be
    implemented.
    """
    def execute(self, sender_list: List[Dict[str, Any]],
                requested_list: List[Dict[str, Any]], pkmn_csv_data: Dict[str,
                Any]) -> bool:
        """
        The blueprint for the execute.

        Args:
            sender_list (List[Dict[str, Any]): The list of Pokemon with
            associated values such as abilities, form, pokeball captured in,
            etc.
            requested_list (List[Dict[str, Any]): The list of Pokemon with
            associated values such as abilities, form, pokeball captured in,
            etc.
            pkmn_csv_data (Dict[str, Any]):  Data of Pokemon marked in a CSV

        Returns:
            bool

        """
        pass
