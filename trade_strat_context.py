from trade_strategy import TradeStrategy

class PokemonTradeContext:
    def __init__(self, strategy: TradeStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: TradeStrategy):
        self._strategy = strategy

    def execute_strategy(self, sender_list, requested_list, csv_data) -> bool:
        return self._strategy.execute(sender_list, requested_list, csv_data)