import oandapyV20
import oandapyV20.endpoints.accounts as accounts

# 1.  credentials
ACCESS_TOKEN = "your_token_here"
ACCOUNT_ID = "your_account_id_here"

# 2. Connect to the practice environment
client = oandapyV20.API(access_token=ACCESS_TOKEN, environment="practice")

try:
    # 3. Request account details
    req = accounts.AccountSummary(accountID=ACCOUNT_ID)
    client.request(req)
    
    # 4. Print the result
    balance = req.response['account']['balance']
    currency = req.response['account']['currency']
    print(f"Connection Successful!")
    print(f"Current Account Balance: {balance} {currency}")

except Exception as e:
    print(f"Connection failed. Error: {e}")
