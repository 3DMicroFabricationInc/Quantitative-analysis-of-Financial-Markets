import yfinance as yf

# Define the ticker symbol
ticker = yf.Ticker("AAPL")

# Get the latest market data
apple_data = ticker.history(period="1d")

# Extract the last closing price
current_price = apple_data['Close'].iloc[-1]

print(f"Apple (AAPL) current stock price: ${current_price:.2f}")

# If you want the real-time price (during market hours), you can use:
# current_price = ticker.info['currentPrice']
# print(f"Apple (AAPL) live price: ${current_price:.2f}")
