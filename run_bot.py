import logging

# Configure professional dual-stream logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("trading_bot.log"),  # Permanently saves logs to this file
        logging.StreamHandler()                 # Continuously outputs logs to your terminal screen
    ]
)

import time
import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.orders as orders
from oandapyV20.contrib.requests import MarketOrderRequest, TakeProfitDetails, StopLossDetails
import pandas as pd

# CONFIGURATION
ACCESS_TOKEN = "your_token_here"
ACCOUNT_ID = "your_account_id_here"
INSTRUMENT = "NAS100_USD"
GRANULARITY = "M30" 
LOOP_INTERVAL = 60   # seconds

# Initialize the OANDA API Client
client = oandapyV20.API(access_token=ACCESS_TOKEN, environment="practice")

# FUNCTIONS
def get_market_candles(instrument, count=5, granularity="M15"):
    """Fetches historical candle data and returns a clean Pandas DataFrame."""
    params = {"count": count, "granularity": granularity, "price": "M"}
    try:
        req = instruments.InstrumentsCandles(instrument=instrument, params=params)
        client.request(req)
        
        candle_data = []
        for candle in req.response['candles']:
            if candle['complete']:
                candle_data.append({
                    "Open": float(candle['mid']['o']),
                    "High": float(candle['mid']['h']),
                    "Low": float(candle['mid']['l']),
                    "Close": float(candle['mid']['c'])
                })
        return pd.DataFrame(candle_data)
    except Exception as e:
        logging.error(f"⚠️ Error fetching data: {e}")
        return pd.DataFrame()  # Return empty DataFrame on failure

def place_bracket_order(instrument, units, stop_loss, take_profit):
    """Sends a market order paired with automatic risk exits to OANDA."""
    try:
        sl_details = StopLossDetails(price=str(stop_loss))
        tp_details = TakeProfitDetails(price=str(take_profit))
        
        order_request = MarketOrderRequest(
            instrument=instrument,
            units=units,  # Positive for Buy, Negative for Sell
            stopLossOnFill=sl_details.data,
            takeProfitOnFill=tp_details.data
        )
        
        req = orders.OrderCreate(accountID=ACCOUNT_ID, data=order_request.data)
        response = client.request(req)
        order_id = response.get('orderFillTransaction', {}).get('id', 'N/A')
        logging.error(f"✔️ Order Executed Successfully! Order ID: {order_id}")
        return response
    except Exception as e:
        logging.error(f"❌ Failed to place order: {e}")
        return None


# MAIN CONTINUOUS EXECUTION LOOP
if __name__ == "__main__":
    logging.info("🚀 Launching OANDA Automated Trading Loop...")
    logging.info(f"Configured for {INSTRUMENT} on {GRANULARITY} charts. checking every {LOOP_INTERVAL} seconds.")
    logging.info("👉 Press Ctrl+C in this terminal at any time to shut down the bot.")
    logging.info("-" * 60)

    while True:
        try:
            logging.info(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Checking market...")
            df = get_market_candles(INSTRUMENT, count=5, granularity=GRANULARITY)

            if not df.empty:
                # Target the most recently closed candle
                latest_candle = df.iloc[-1]
                current_close = latest_candle['Close']
                current_open = latest_candle['Open']
                
                logging.info(f"Latest Candle Status -> Open: {current_open} | Close: {current_close}")
                
                # --- STRATEGY LOGIC ENGINE ---
                if current_close > current_open:
                    logging.info("🟢 Bullish signal detected. Preparing trade entry...")
                    
                    entry_price = current_close
                    # Format strictly to 5 decimal places for OANDA compliance
                    target_sl = "{:.2f}".format(entry_price - 20.00)  # Stop loss 
                    target_tp = "{:.2f}".format(entry_price + 40.00)  # Take profit
                    trade_size = 1000  # 1 micro-lot
                    
                    logging.info(f"Sending Order: Buy {trade_size} units | SL: {target_sl} | TP: {target_tp}")
                    place_bracket_order(INSTRUMENT, trade_size, target_sl, target_tp)
                else:
                    logging.info("⚪ Conditions not met (Bearish or Flat candle). No trades taken.")
            else:
                logging.info("⚠️ Retrying next cycle due to missing candle payload data.")

        except Exception as loop_error:
            # Prevents issues
            logging.info(f"⚠️ Unexpected loop interruption: {loop_error}")

        # Pause the loopsafely
        logging.info(f"Sleeping for {LOOP_INTERVAL} seconds...")
        time.sleep(LOOP_INTERVAL)
