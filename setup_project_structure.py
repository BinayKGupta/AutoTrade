import os

def create_project_structure(base_dir="etrade_trading_bot"): 
    folders = [ "config", "data/historical", "data/live_ticks", "strategies", "execution", "risk", "scheduler", "utils", "backtesting" ]
    try:
        print("Hello")
        for folder in folders:
            path = os.path.join(base_dir, folder)
            os.makedirs(path, exist_ok=True)
            print(f"✅ Created: {path}")

        # Create placeholder files
        placeholder_files = [
            "config/credentials.yaml",
            "strategies/base_strategy.py",
            "strategies/ema_crossover.py",
            "execution/etrade_order_manager.py",
            "risk/risk_manager.py",
            "scheduler/job_runner.py",
            "utils/data_fetcher.py",
            "utils/logger.py",
            "utils/auth_manager.py",
            "backtesting/backtest_engine.py",
            "main.py",
            "requirements.txt"
        ]

        for file in placeholder_files:
            file_path = os.path.join(base_dir, file)
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    f.write("# Placeholder\n")
                print(f"📄 Created: {file_path}")

        print("\n🚀 Project structure setup complete!")

    except Exception as e:
        print(f"❌ Error while creating project structure: {e}")

 

if __name__ == "__main__":
    print("Hello, World!")
    create_project_structure()
