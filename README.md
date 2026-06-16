# Automated Pivot Point Trading Bot

An automated, algorithmic trading execution engine that connects to the OANDA v20 REST API. This system translates intraday technical indicators into live order execution payloads, engineered specifically for index CFDs (`NAS100_USD`).

## 🚀 System Architecture & Flow

This code operates on a continuous execution loop using a decoupled design to safely manage data processing and order dispatching:

1. **Data Ingestion Module:** Authenticates securely via environment variables to pull real-time midpoint candle historical data sets from OANDA.
2. **Strategy Analytics Engine:** Processes historical dataframes to calculate daily Pivot Points, Resistance (R1), and Support (S1) boundaries. It dynamically replicates programmatic Pine Script crossover/crossunder functions.
3. **Risk Management & Dispatcher:** Formats financial asset precision strings and dispatches market orders alongside automatic protective bracket exits (Stop Loss and Take Profit).

## 🛠️ Tech Stack & Dependencies

* **Language:** Python 3.11+
* **Data Processing:** Pandas (DataFrame manipulation and analytical slicing)
* **API Wrapper:** oandapyV20 (REST API communication)
* **Security:** python-dotenv (Runtime environment variable encapsulation)

## 📦 Local Installation & Setup

1. Clone the repository:
   ```bash
1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/nasdaq-pivot-trading-bot.git](https://github.com/YOUR_USERNAME/nasdaq-pivot-trading-bot.git)
   cd nasdaq-pivot-trading-bot
