import stock_data
import csv
from stock import Stock, DailyData
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

class StockConsole:
    def __init__(self):
        self.stock_list = []

    def display_main_menu(self):
        print("\nStock Analyzer ----")
        print("1 - Manage Stocks (Add, Update, Delete, List)")
        print("2 - Add Daily Stock Data (Date, Price, Volume)")
        print("3 - Show Report")
        print("4 - Show Chart")
        print("5 - Manage Data (Save, Load, Retrieve)")
        print("0 - Exit Program")
        return input("Enter Menu Option: ")

    def manage_stocks_menu(self):
        while True:
            print("\nManage Stocks ----")
            print("1 - Add Stock")
            print("2 - Update Shares")
            print("3 - Delete Stock")
            print("4 - List Stocks")
            print("0 - Exit Manage Stocks")
            choice = input("Enter Menu Option: ")
            
            if choice == "1":
                self.add_stock()
            elif choice == "2":
                self.update_shares_menu()
            elif choice == "3":
                self.delete_stock()
            elif choice == "4":
                self.list_stocks()
            elif choice == "0":
                break
            else:
                print("Invalid option. Please try again.")

    def add_stock(self):
        print("\nAdd Stock ----")
        symbol = input("Enter Ticker Symbol: ").strip().upper()
        name = input("Enter Company Name: ").strip().upper()
        try:
            shares = float(input("Enter Number of Shares: "))
            if shares < 0:
                raise ValueError("Shares cannot be negative")
            stock = Stock(symbol, name, shares)
            self.stock_list.append(stock)
            print("Stock Added - Enter to Add Another Stock or 0 to Stop: ", end="")
            if input() == "0":
                return
        except ValueError as e:
            print(f"Error: {e}. Please try again.")

    def update_shares_menu(self):
        while True:
            print("\nUpdate Shares ----")
            print("1 - Buy Shares")
            print("2 - Sell Shares")
            print("0 - Exit Update Shares")
            choice = input("Enter Menu Option: ")
            
            if choice == "1":
                self.buy_shares()
            elif choice == "2":
                self.sell_shares()
            elif choice == "0":
                break
            else:
                print("Invalid option. Please try again.")

    def buy_shares(self):
        print("\nBuy Shares ----")
        if not self.stock_list:
            print("No stocks available.")
            return
        print(f"Stock List: {[stock.symbol for stock in self.stock_list]}")
        symbol = input("Which stock do you want to buy?: ").strip().upper()
        for stock in self.stock_list:
            if stock.symbol == symbol:
                try:
                    shares = float(input("How many shares do you want to buy?: "))
                    if shares <= 0:
                        raise ValueError("Shares must be positive")
                    stock.shares += shares
                    print(f"Updated shares for {symbol}: {stock.shares}")
                    return
                except ValueError as e:
                    print(f"Error: {e}. Please try again.")
                    return
        print(f"Stock {symbol} not found.")

    def sell_shares(self):
        print("\nSell Shares ----")
        if not self.stock_list:
            print("No stocks available.")
            return
        print(f"Stock List: {[stock.symbol for stock in self.stock_list]}")
        symbol = input("Which stock do you want to sell?: ").strip().upper()
        for stock in self.stock_list:
            if stock.symbol == symbol:
                try:
                    shares = float(input("How many shares do you want to sell?: "))
                    if shares <= 0:
                        raise ValueError("Shares must be positive")
                    if shares > stock.shares:
                        raise ValueError("Cannot sell more shares than you own")
                    stock.shares -= shares
                    print(f"Updated shares for {symbol}: {stock.shares}")
                    return
                except ValueError as e:
                    print(f"Error: {e}. Please try again.")
                    return
        print(f"Stock {symbol} not found.")

    def delete_stock(self):
        print("\nDelete Stock ----")
        if not self.stock_list:
            print("No stocks available.")
            return
        print(f"Stock List: {[stock.symbol for stock in self.stock_list]}")
        symbol = input("Which stock do you want to delete?: ").strip().upper()
        for i, stock in enumerate(self.stock_list):
            if stock.symbol == symbol:
                self.stock_list.pop(i)
                print(f"Stock {symbol} deleted.")
                return
        print(f"Stock {symbol} not found.")

    def list_stocks(self):
        print("\nStock List ----")
        if not self.stock_list:
            print("No stocks available.")
            input("Press Enter to Continue ***")
            return
        print("SYMBOL\tNAME\t\tSHARES")
        for stock in self.stock_list:
            print(f"{stock.symbol}\t{stock.name}\t\t{stock.shares}")
        input("Press Enter to Continue ***")

    def add_daily_stock_data(self):
        print("\nAdd Daily Stock Data ----")
        if not self.stock_list:
            print("No stocks available.")
            return
        print(f"Stock List: {[stock.symbol for stock in self.stock_list]}")
        symbol = input("Which stock do you want to use?: ").strip().upper()
        for stock in self.stock_list:
            if stock.symbol == symbol:
                print(f"Fetching data for: {stock.symbol}")
                dateFrom = input("Enter starting date (MM/DD/YY): ")
                dateTo = input("Enter ending date (MM/DD/YY): ")
                try:
                    record_count = stock_data.retrieve_stock_web(dateFrom, dateTo, [stock])
                    print(f"\nData fetched for {stock.symbol} ({record_count} records):")
                    if stock.daily_data:
                        print("Date\t\tPrice\t\tVolume")
                        for data in stock.daily_data:
                            print(f"{data.date}\t{data.closing_price}\t{data.volume}")
                    else:
                        print("No data retrieved.")
                    input("Press Enter to Continue ***")
                    return
                except Exception as e:
                    print(f"Error fetching data: {str(e)}")
                    input("Press Enter to Continue ***")
                    return
        print(f"Stock {symbol} not found.")

    def show_report(self):
        print("\nStock Report ----")
        if not self.stock_list:
            print("No stocks available.")
            input("---- Report Complete ----\nPress Enter to Continue")
            return
        for stock in self.stock_list:
            print(f"Report for: {stock.symbol} {stock.name}")
            print(f"Shares: {stock.shares}")
            if not stock.daily_data:
                print("*** No daily history.")
            else:
                for data in stock.daily_data:
                    print(f"Date: {data.date}, Price: {data.closing_price}, Volume: {data.volume}")
        input("---- Report Complete ----\nPress Enter to Continue")

    def show_chart(self):
        print("\nShow Chart ----")
        if not self.stock_list:
            print("No stocks available.")
            return
        print(f"Stock List: {[stock.symbol for stock in self.stock_list]}")
        symbol = input("Which stock do you want to use?: ").strip().upper()
        for stock in self.stock_list:
            if stock.symbol == symbol:
                if not stock.daily_data:
                    print("No daily data available to plot.")
                    return
                dates = []
                prices = []
                for data in stock.daily_data:
                    try:
                        date = datetime.strptime(data.date, "%m/%d/%y")
                        dates.append(date)
                        prices.append(data.closing_price)
                    except ValueError as e:
                        print(f"Error parsing date {data.date}: {e}. Skipping this entry.")
                        continue
                
                if not dates:
                    print("No valid data to plot.")
                    return
                
                plt.figure(figsize=(10, 6))
                plt.plot(dates, prices, 'b-', label=f"{stock.name} Price")
                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
                plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
                plt.gcf().autofmt_xdate()
                plt.xlabel("Date")
                plt.ylabel("Price")
                plt.title(stock.name)
                plt.grid(True)
                plt.legend()
                plt.savefig(f"{stock.symbol}_price_chart.png")
                plt.show()
                return
        print(f"Stock {symbol} not found.")

    def manage_data_menu(self):
        while True:
            print("\nManage Data ----")
            print("1 - Save Data to Database")
            print("2 - Load Data from Database")
            print("3 - Retrieve Data from Web")
            print("4 - Import from CSV File")
            print("0 - Exit Manage Data")
            choice = input("Enter Menu Option: ")
            
            if choice == "1":
                self.save_to_database()
            elif choice == "2":
                self.load_from_database()
            elif choice == "3":
                self.retrieve_from_web()
            elif choice == "4":
                self.import_csv()
            elif choice == "0":
                break
            else:
                print("Invalid option. Please try again.")

    def save_to_database(self):
        print("Saving to database...")
        dateFrom = "01/01/25"  # Arbitrary start date
        dateTo = "12/31/25"    # Arbitrary end date
        try:
            stock_data.retrieve_stock_web(dateFrom, dateTo, self.stock_list)
            temp_filename = "temp_stock_data.csv"
            with open(temp_filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Symbol", "Date", "Price", "Volume"])  # Header
                for stock in self.stock_list:
                    for data in stock.daily_data:
                        writer.writerow([stock.symbol, data.date, data.closing_price, data.volume])
            print("Data saved to temporary file. Please enter a filename to save permanently:")
            filename = input("Enter filename: ").strip()
            if filename:
                import shutil
                shutil.move(temp_filename, filename + ".csv")
                print(f"Data saved to {filename}.csv")
            else:
                print("No filename provided, data saved as temp_stock_data.csv")
            input("Press Enter to Continue")
        except Exception as e:
            print(f"Error saving data: {str(e)}")
            input("Press Enter to Continue")

    def load_from_database(self):
        print("\n---- Data Loaded from Database ----")
        try:
            filename = input("Enter CSV filename to load: ").strip()
            if not filename.endswith('.csv'):
                filename += '.csv'
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                symbol = input("Enter stock symbol to load: ").strip().upper()
                dateFrom = input("Enter starting date (MM/DD/YY): ")
                dateTo = input("Enter ending date (MM/DD/YY): ")
                start_date = datetime.strptime(dateFrom, "%m/%d/%y")
                end_date = datetime.strptime(dateTo, "%m/%d/%y")
                for stock in self.stock_list:
                    if stock.symbol == symbol:
                        stock.daily_data = []  # Clear existing data
                        for row in reader:
                            if row[0] == symbol:  # Match stock symbol
                                row_date = datetime.strptime(row[1], "%m/%d/%y")
                                if start_date <= row_date <= end_date:
                                    daily_data = DailyData(row[1], float(row[2]), int(row[3]))
                                    stock.add_daily_data(daily_data)
                        print(f"\nData loaded for {symbol} within {dateFrom} to {dateTo}:")
                        if stock.daily_data:
                            print("Date\t\tPrice\t\tVolume")
                            for data in stock.daily_data:
                                print(f"{data.date}\t{data.closing_price}\t{data.volume}")
                        else:
                            print("No data found for the specified date range.")
                        break
                else:
                    print(f"Stock {symbol} not found in portfolio")
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print(f"Error loading data: {str(e)}")
        input("Press Enter to Continue")

    def retrieve_from_web(self):
        print("\nRetrieving Stock Data from Yahoo! Finance ----")
        print("This will retrieve data from all stocks in your stock list.")
        dateFrom = input("Enter starting date (MM/DD/YY): ")
        dateTo = input("Enter ending date (MM/DD/YY): ")
        try:
            record_count = stock_data.retrieve_stock_web(dateFrom, dateTo, self.stock_list)
            print(f"Records Retrieved: {record_count}")
        except Exception as e:
            print(f"Error retrieving data: {str(e)}")
        input("Press Enter to Continue")

    def import_csv(self):
        print("\nImport CSV file from Yahoo! Finance ----")
        try:
            filename = input("Enter CSV filename to load: ").strip()
            if not filename.endswith('.csv'):
                filename += '.csv'
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                symbol = input("Enter stock symbol to load: ").strip().upper()
                dateFrom = input("Enter starting date (MM/DD/YY): ")
                dateTo = input("Enter ending date (MM/DD/YY): ")
                start_date = datetime.strptime(dateFrom, "%m/%d/%y")
                end_date = datetime.strptime(dateTo, "%m/%d/%y")
                for stock in self.stock_list:
                    if stock.symbol == symbol:
                        stock.daily_data = []  # Clear existing data
                        for row in reader:
                            if row[0] == symbol:  # Match stock symbol
                                row_date = datetime.strptime(row[1], "%m/%d/%y")
                                if start_date <= row_date <= end_date:
                                    daily_data = DailyData(row[1], float(row[2]), int(row[3]))
                                    stock.add_daily_data(daily_data)
                        print(f"\nData loaded for {symbol} within {dateFrom} to {dateTo}:")
                        if stock.daily_data:
                            print("Date\t\tPrice\t\tVolume")
                            for data in stock.daily_data:
                                print(f"{data.date}\t{data.closing_price}\t{data.volume}")
                        else:
                            print("No data found for the specified date range.")
                        break
                else:
                    print(f"Stock {symbol} not found in portfolio")
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print(f"Error loading data: {str(e)}")
        input("Press Enter to Continue")

    def run(self):
        while True:
            choice = self.display_main_menu()
            if choice == "1":
                self.manage_stocks_menu()
            elif choice == "2":
                self.add_daily_stock_data()
            elif choice == "3":
                self.show_report()
            elif choice == "4":
                self.show_chart()
            elif choice == "5":
                self.manage_data_menu()
            elif choice == "0":
                print("Exiting program...")
                break
            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    app = StockConsole()
    app.run()