# Placeholder
import datetime 
import logging

class RiskManager: 
    """ Simple risk management layer. Checks conditions before allowing a trade. Extend this for position sizing, exposure limits, P&L protection, etc. """
    def __init__(self, max_position_size=100, allowed_symbols=None):
        self.max_position_size = max_position_size
        self.allowed_symbols = allowed_symbols if allowed_symbols else ["AAPL", "MSFT", "TSLA"]
        self.logger = logging.getLogger("RiskManager")

    def _is_market_open(self):
        """
        Dummy check: Only allow trades between 9:30 and 16:00 Eastern.
        Replace this with an exchange API call if you want accurate status.
        """
        now = datetime.datetime.now()
        market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
        market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
        return market_open <= now <= market_close

    def is_trade_allowed(self, signal):
        """
        Evaluates the incoming trade signal.
        :param signal: dict — output from your strategy.
        :return: True if trade is allowed, False otherwise.
        """

        if not signal:
            self.logger.warning("No valid signal data provided.")
            return False

        if signal["action"] == "HOLD":
            return False

        # Symbol check (assuming signal has symbol field)
        symbol = signal.get("symbol", "AAPL")
        if symbol not in self.allowed_symbols:
            self.logger.warning(f"Symbol {symbol} is not allowed for trading.")
            return False

        # Market hours check
        if not self._is_market_open():
            self.logger.warning("Market is closed. Blocking trade.")
            return False

        # Position size / risk limit check
        desired_size = signal.get("size", 1)
        if desired_size > self.max_position_size:
            self.logger.warning(f"Trade size {desired_size} exceeds max limit {self.max_position_size}.")
            return False

        self.logger.info("Risk check passed — trade allowed.")
        return True
    
if __name__ == "__main__":
    # Example usage 
    risk = RiskManager() 
    dummy_signal = {"action": "BUY", "symbol": "AAPL", "size": 10} 
    allowed = risk.is_trade_allowed(dummy_signal) 
    print(f"Trade Allowed: {allowed}")
    print("Start")