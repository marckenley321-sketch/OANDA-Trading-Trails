import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import pandas as pd

# Credentials
ACCESS_TOKEN = "db3929e7cd5160f21964aeeebc9a4865-6daccc3e99178f3aad941715be2c73ba"
ACCOUNT_ID = "101-001-39314361-001"

client = oandapyV20.API(access_token=ACCESS_TOKEN, environment="practice")

def get_market_candles(instrument, count=5, granularity="M15"):
    params = {
        "count": count,
        "granularity": granularity,  # M15 = 15 Minute candles, H1 = 1 Hour, etc.
        "price": "M"                 # "M" fetches Midpoint prices (average of Bid/Ask)
    }
    
    try:
        req = instruments.InstrumentsCandles(instrument=instrument, params=params)
        client.request(req)
        
        # Parse the raw JSON into a clean list
        candle_data = []
        for candle in req.response['candles']:
            if candle['complete']:  # Only grab closed, finished candles
                candle_data.append({
                    "Time": candle['time'],
                    "Open": float(candle['mid']['o']),
                    "High": float(candle['mid']['h']),
                    "Low": float(candle['mid']['l']),
                    "Close": float(candle['mid']['c']),
                    "Volume": int(candle['volume'])
                })
        
        # Turn it into a beautiful Pandas DataFrame for calculations
        df = pd.DataFrame(candle_data)
        return df

    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# Run the function for EUR/USD
df_candles = get_market_candles("EUR_USD", count=5, granularity="M15")

if df_candles is not None:
    print("\n--- Latest Closed 15-Minute Candles ---")
    print(df_candles)