import oandapyV20
import oandapyV20.endpoints.accounts as accounts

# 1.  credentials
ACCESS_TOKEN = "db3929e7cd5160f21964aeeebc9a4865-6daccc3e99178f3aad941715be2c73ba"
ACCOUNT_ID = "101-001-39314361-001"

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