import requests

# Alpha Vantage API Key
API_KEY = 'YOUR_API_KEY'

# Function to fetch stock price using Alpha Vantage API
def get_stock_price(symbol):
    """Fetches real-time stock price for a given symbol."""
    url = f'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '5min',
        'apikey': API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    # Check if API call is successful
    if "Time Series (5min)" in data:
        latest_time = list(data["Time Series (5min)"].keys())[0]
        latest_data = data["Time Series (5min)"][latest_time]
        return float(latest_data["4. close"])
    else:
        print("Error fetching stock data.")
        return None

# Portfolio class to manage user's stock investments
class Portfolio:
    def __init__(self):
        self.stocks = {}

    def add_stock(self, symbol, shares):
        """Adds a stock to the portfolio."""
        if symbol in self.stocks:
            self.stocks[symbol] += shares
        else:
            self.stocks[symbol] = shares
        print(f"Added {shares} shares of {symbol} to your portfolio.")

    def remove_stock(self, symbol, shares):
        """Removes stock from the portfolio."""
        if symbol in self.stocks and self.stocks[symbol] >= shares:
            self.stocks[symbol] -= shares
            if self.stocks[symbol] == 0:
                del self.stocks[symbol]
            print(f"Removed {shares} shares of {symbol} from your portfolio.")
        else:
            print(f"Error: You don't have enough shares of {symbol}.")

    def display_portfolio(self):
        """Displays the current portfolio with stock details."""
        if not self.stocks:
            print("Your portfolio is empty.")
        else:
            print("\nCurrent Portfolio:")
            for symbol, shares in self.stocks.items():
                price = get_stock_price(symbol)
                if price:
                    value = shares * price
                    print(f"{symbol}: {shares} shares, Current Price: ${price:.2f}, Total Value: ${value:.2f}")
                else:
                    print(f"{symbol}: {shares} shares, Error retrieving price.")

    def portfolio_value(self):
        """Calculates and returns the total value of the portfolio."""
        total_value = 0
        for symbol, shares in self.stocks.items():
            price = get_stock_price(symbol)
            if price:
                total_value += shares * price
        return total_value

# Main function to interact with the user
def main():
    portfolio = Portfolio()
    
    while True:
        print("\nOptions:")
        print("1. Add stock to portfolio")
        print("2. Remove stock from portfolio")
        print("3. View portfolio")
        print("4. View total portfolio value")
        print("5. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            symbol = input("Enter stock symbol (e.g., AAPL): ").upper()
            shares = int(input("Enter number of shares: "))
            portfolio.add_stock(symbol, shares)
        
        elif choice == '2':
            symbol = input("Enter stock symbol to remove (e.g., AAPL): ").upper()
            shares = int(input("Enter number of shares to remove: "))
            portfolio.remove_stock(symbol, shares)
        
        elif choice == '3':
            portfolio.display_portfolio()
        
        elif choice == '4':
            total_value = portfolio.portfolio_value()
            print(f"Total Portfolio Value: ${total_value:.2f}")
        
        elif choice == '5':
            print("Exiting the program.")
            break
        
        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    main()
