from logging import config
import sys
import json
from matplotlib.ticker import MultipleLocator
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
from pathlib import Path

def display_plot(df, stock_name, crossovers, directory_name, end_date):
    # Plot with crossover markers
    
    # figsize=(10, 6) means 10 inches wide and 6 inches tall.
    plt.figure(figsize=(12,5))
    plt.plot(df['High'], label='Daily MSFT High Price', color='blue')
    plt.plot(df['Low'], label='Daily MSFT Low Price', color='red')
    plt.plot(df['Close'], label='Daily MSFT Close Price', color='black')
    plt.plot(df['MA50'], label='50-day MA', color='brown')
    plt.plot(df['MA20'], label='20-day MA', color='green')
    #plt.plot(df['MA10'], label='10-day MA', color='orange')
    plt.plot(df['MA5'], label='5-day MA', color='orange')

    # Mark crossover points
    plt.scatter(crossovers.index, crossovers['Close'], 
            color='black', marker='o', label='Crossovers (moving above/below MA20)')

    plt.title(f"{stock_name} Stock: Market Trend Analysis with Moving Averages")
    plt.xlabel("Date")
    # show a tick every 5 units
    ax = plt.gca()
    ax.xaxis.set_major_locator(MultipleLocator(1))
    # 3. Rotate labels for readability
    plt.xticks(rotation=45)
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True)
    # Adjust layout to prevent overlap
    plt.tight_layout()
    # Save the figure automatically
    plt.savefig(f"{directory_name}{stock_name}_market_trend_{end_date}_plot.png", dpi=300, bbox_inches="tight")
    plt.show()

def new_company():

    # Program to take a text string as input from the user
    prompt="Enter full company name  : "
    try:
        # Read input from the user
        company_name = input(prompt).strip()  # Remove leading/trailing spaces
        
        # Validate that the input is not empty
        if not company_name:
            print("Error: You must enter a company name.")
            return None
        
    except (EOFError, KeyboardInterrupt):
        # Handle cases where the user interrupts input
        print("\nInput cancelled by user.")
        exit(0)
        return None
    
    # Program to take a text string as input from the user
    prompt="Enter shortened company name  : "
    try:
        # Read input from the user
        company_short_name = input(prompt).strip().lower()  # Remove leading/trailing spaces
        
        # Validate that the input is not empty
        if not company_short_name:
            print("Error: You must enter a shortened company name.")
            return None
        
    except (EOFError, KeyboardInterrupt):
        # Handle cases where the user interrupts input
        print("\nInput cancelled by user.")
        exit(0)
        return None
    
    prompt="Enter company code  : "
    try:
        # Read input from the user
        company_code = input(prompt).strip()  # Remove leading/trailing spaces
        
        # Validate that the input is not empty
        if not company_code:
            print("Error: You must enter a company code.")
            return None
        
    except (EOFError, KeyboardInterrupt):
        # Handle cases where the user interrupts input
        print("\nInput cancelled by user.")
        exit(0)
        return None

    # Load JSON file
    with open("config.json", "r") as f:
        config = json.load(f)
    
    # Convert JSON to DataFrame
    #df = pd.DataFrame(config["stocks"])

    # New company entry
    new_company = {
        "company": f"{company_name}",
        "details": {
            "name": company_short_name,
            "code": company_code
        }
    }
    
    # Insert new company into JSON document
    config["stocks"].append(new_company)

    # Save back to file (optional)
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    # Create a single directory
    directory_name = f"./{new_company['details']['name']}/"
    Path(directory_name).mkdir(exist_ok=True)

    new_company = {
        "stock_name": f"{company_name}",
        "ticker": f"{company_code}",
        "start_date": "2026-02-02",
        "end_date": "2026-04-22"
    }

    # Save new company config to its own JSON file
    # Save back to file (optional)
    with open(f"{directory_name}config.json", "w") as f:
        json.dump(new_company, f, indent=4)

        
    print("Updated JSON:")
    print(json.dumps(config, indent=4))

def get_data(directory_name):
    # Load JSON file
    with open(f"{directory_name}config.json", "r") as f:
        config = json.load(f)

    # Extract values from JSON
    stock_name = config["stock_name"]
    start_date = config["start_date"]
    end_date = datetime.today().strftime('%Y-%m-%d')
    #end_date = config["end_date"]
    #end_date = "2026-01-01"
    ticker = config["ticker"]
    
    # Download Microsoft stock data
    ticker_val = yf.download(ticker, start=start_date, end=end_date)

    # Check if data was downloaded successfully
    if ticker_val is None:
        print("Failed to download data.")
        exit(0)
    else:
        print("Data downloaded successfully.")
        df = pd.DataFrame(ticker_val)

        # Rename columns to standard names
        df.columns = ["Open", "High", "Low", "Close", "Volume"]

        # 1. Calculate MA directly into the DataFrame
        # By default, rolling() will produce NaN for the first (window-1) rows.
        #df['MA20'] = df['Close'].rolling(window=20).mean()
        df['MA50'] = df['Close'].rolling(window=50, min_periods=1).mean()
        df['MA20'] = df['Close'].rolling(window=20, min_periods=1).mean()
        df['MA10'] = df['Close'].rolling(window=10, min_periods=1).mean()
        df['MA5'] = df['Close'].rolling(window=5, min_periods=1).mean()
                
        # Difference between Close and MA20
        df['Diff_Close_MA20'] = df['Close'] - df['MA20']

        # Save to CSV for debugging
        df.to_csv(f"{directory_name}{stock_name}_stock_data.csv")

        # Signals
        df['Signal'] = 0
        df.loc[df['Close'] > df['MA20'], 'Signal'] = 1
        df.loc[df['Close'] < df['MA20'], 'Signal'] = -1

        # Crossovers
        df['Crossover'] = df['Signal'].diff()

        # Filter crossover points
        crossovers = df[df['Crossover'].isin([2, -2])]
        print(crossovers[['Close', 'MA20', 'Crossover']])
        # Save to CSV for debugging
        crossovers.to_csv(f"{directory_name}{stock_name}_crossover_data.csv")

        display_plot(df, stock_name, crossovers, directory_name, end_date)

class SimpleAgent:
    def __init__(self, name="HelperBot"):
        self.my_var = None
        # Load JSON file
        with open("config.json", "r") as f:
            config = json.load(f)
        
        # Convert JSON to DataFrame
        df = pd.DataFrame(config["stocks"])

        # Count the number of companies
        company_count = len(df)

        print("Number of companies:", company_count)

        self.name = name
        self.commands = {
            
            f"{config['stocks'][i]['details']['name']}": self.show_config
            for i in range(company_count)     
        }
        
    def show_config(self):
        """Show the configuration."""
        print(self.my_var)
        if self.my_var == "help":
            return self.show_help()
        elif self.my_var == "exit":
            return self.exit_agent()
        elif self.my_var == "new_company":
            return new_company()
        elif self.my_var == "reload":
            return SimpleAgent().run()
        
        directory_name = f"./{self.my_var}/"
        get_data(directory_name)
         
    def show_help(self):
        """List available commands."""
        return "Available commands: " + ", ".join(self.commands.keys())

    def exit_agent(self):
        """Exit the agent."""
        print("Goodbye!")
        sys.exit(0)

    def handle_input(self, user_input):
        """Process user input and return a response."""
        user_input = user_input.strip().lower()
        if user_input in self.commands:
            self.my_var = user_input
            return self.commands[user_input]()
        else:
            return f"I don't understand '{user_input}'. Type 'help' for options."

    def run(self):
        """Run the agent loop."""
        print(f"{self.name} is ready! Type 'help' for commands.")
        while True:
            try:
                user_input = input("> ")
                response = self.handle_input(user_input)
                print(response)
            except KeyboardInterrupt:
                print("\nInterrupted. Exiting...")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    agent = SimpleAgent()
    agent.run()

