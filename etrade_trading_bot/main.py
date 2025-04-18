# Placeholder
import signal 
import sys 
import time 
from strategies.ema_crossover import EMACrossoverStrategy 
from execution.etrade_order_manager import ETradeOrderManager 
from risk.risk_manager import RiskManager 
from utils.data_fetcher import MarketDataFetcher 
from utils.logger import setup_logger

logger = setup_logger('trade_bot')
shutdown_flag = False

def signal_handler(sig, frame): 
    global shutdown_flag 
    logger.info("Shutdown signal received.") 
    shutdown_flag = True

signal.signal(signal.SIGINT, signal_handler) # Ctrl+C signal.signal(signal.SIGTERM, signal_handler) # kill signal

def main(): 
    logger.info("Starting E*TRADE Automated Trading Bot...")
    # Initialize components
    order_manager = ETradeOrderManager()
    risk_manager = RiskManager()
    strategy = EMACrossoverStrategy()
    data_fetcher = MarketDataFetcher()

    # Warm-up / Initialization
    logger.info("Initializing strategy and fetching initial data...")
    strategy.initialize()

    try:
        while not shutdown_flag:
            # Fetch latest market data
            market_data = data_fetcher.get_latest()

            if not market_data:
                logger.warning("No market data available, retrying...")
                time.sleep(2)
                continue

            # Generate trade signal
            signal_decision = strategy.generate_signal(market_data)

            if signal_decision:
                logger.info(f"Strategy Signal: {signal_decision}")

                # Risk check before order execution
                if risk_manager.is_trade_allowed(signal_decision):
                    order_manager.execute_order(signal_decision)
                else:
                    logger.info("Risk manager blocked the trade.")

            # Loop control to avoid API overuse
            time.sleep(1)  # Adjust this depending on strategy speed

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")

    finally:
        logger.info("Shutting down trading bot gracefully...")
        order_manager.close_all_positions()
        logger.info("All positions closed. Exiting.")

if __name__ == "__main__":
    print("Start!")
    main()
