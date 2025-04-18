# Placeholder
import pandas as pd 
import numpy as np

class EMACrossoverStrategy: 
    """ A simple Exponential Moving Average (EMA) crossover strategy. Generates BUY / SELL / HOLD signals based on two EMAs. """
    def __init__(self, fast_period=12, slow_period=26):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.last_signal = None

    def initialize(self):
        """
        Initialization logic if needed (e.g., warm-up data check).
        """
        print("[Strategy] EMACrossoverStrategy initialized.")

    def generate_signal(self, market_data):
        """
        Accepts market_data as a list or pandas Series of recent closing prices.
        Returns a dictionary with signal details: BUY, SELL, or HOLD.
        """

        if len(market_data) < self.slow_period:
            print("[Strategy] Not enough data to compute EMAs.")
            return None

        data_series = pd.Series(market_data)

        fast_ema = data_series.ewm(span=self.fast_period, adjust=False).mean()
        slow_ema = data_series.ewm(span=self.slow_period, adjust=False).mean()

        # Current and previous crossover conditions
        if fast_ema.iloc[-2] < slow_ema.iloc[-2] and fast_ema.iloc[-1] > slow_ema.iloc[-1]:
            signal = 'BUY'
        elif fast_ema.iloc[-2] > slow_ema.iloc[-2] and fast_ema.iloc[-1] < slow_ema.iloc[-1]:
            signal = 'SELL'
        else:
            signal = 'HOLD'

        if signal != 'HOLD':
            self.last_signal = signal

        return {
            "action": signal,
            "price": data_series.iloc[-1],
            "fast_ema": fast_ema.iloc[-1],
            "slow_ema": slow_ema.iloc[-1]
        }

if __name__ == "__main__":
    print("Start!")
    # Quick test 
    #dummy_prices = np.random.normal(100, 1, 50).tolist() 
    #strategy = EMACrossoverStrategy() 
    #strategy.initialize() 
    #signal = strategy.generate_signal(dummy_prices) 
    # print(f"Generated Signal: {signal}")