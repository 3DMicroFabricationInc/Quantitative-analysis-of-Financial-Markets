import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime

def display_plot():
    # Plot with crossover markers
    plt.figure(figsize=(12,6))
    plt.plot(df['Close'], label='AAPL Close Price', color='blue')
    plt.plot(df['MA20'], label='20-day MA', color='red')

    # Mark crossover points
    plt.scatter(crossovers.index, crossovers['Close'], 
            color='black', marker='o', label='Crossovers')

    plt.title("Apple Stock: Close vs 20-day MA")
    plt.xlabel("Date")
    # 3. Rotate labels for readability
    plt.xticks(rotation=45)
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True)
    plt.show()

start_date = "2026-01-02"
end_date = datetime.today().date()

# Download Apple stock data
aapl = yf.download("AAPL", start=start_date, end=end_date)

if aapl is None:
    print("Failed to download data.")
    exit(0)
else:
    print("Data downloaded successfully.")
    df = pd.DataFrame(aapl)
   
    df.columns = ["Open", "High", "Low", "Close", "Volume"]

    # 1. Calculate MA directly into the DataFrame
    #df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA20'] = df['Close'].rolling(window=20, min_periods=1).mean()
            
    # Difference between Close and MA20
    df['Diff_Close_MA20'] = df['Close'] - df['MA20']

    df.to_csv("apple_stock_data.csv")  # Save to CSV for debugging

    # Signals
    df['Signal'] = 0
    df.loc[df['Close'] > df['MA20'], 'Signal'] = 1
    df.loc[df['Close'] < df['MA20'], 'Signal'] = -1

    # Crossovers
    df['Crossover'] = df['Signal'].diff()

    # Filter crossover points
    crossovers = df[df['Crossover'].isin([2, -2])]
    print(crossovers[['Close', 'MA20', 'Crossover']])

    display_plot()
   

    
    

    

    

    

    
    

    
    

    
    

    
    




    
