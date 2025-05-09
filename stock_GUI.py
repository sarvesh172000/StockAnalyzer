import stock_data
import csv
from stock import Stock, DailyData
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog

class StockGUI:
    def __init__(self, root):
        self.stock_list = []
        self.root = root
        self.root.title("Stock Analyzer")
        self.root.geometry("600x400")

        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        ttk.Label(self.main_frame, text="Stock Analyzer By Sarvesh", font=("Arial", 16, "bold")).pack(pady=10)

        # Buttons for main menu
        ttk.Button(self.main_frame, text="Manage Stocks", command=self.manage_stocks_menu).pack(fill=tk.X, pady=5)
        ttk.Button(self.main_frame, text="Add Daily Stock Data", command=self.add_daily_stock_data).pack(fill=tk.X, pady=5)
        ttk.Button(self.main_frame, text="Show Report", command=self.show_report).pack(fill=tk.X, pady=5)
        ttk.Button(self.main_frame, text="Show Chart", command=self.show_chart).pack(fill=tk.X, pady=5)
        ttk.Button(self.main_frame, text="Manage Data", command=self.manage_data_menu).pack(fill=tk.X, pady=5)
        ttk.Button(self.main_frame, text="Exit Program", command=self.root.quit).pack(fill=tk.X, pady=5)

        # Output area
        self.output_text = tk.Text(self.main_frame, height=10, width=60, state='disabled')
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=10)

    def display_output(self, message):
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, message)
        self.output_text.config(state='disabled')

    def manage_stocks_menu(self):
        manage_window = tk.Toplevel(self.root)
        manage_window.title("Manage Stocks")
        manage_window.geometry("400x300")

        ttk.Label(manage_window, text="Manage Stocks", font=("Arial", 14, "bold")).pack(pady=10)

        ttk.Button(manage_window, text="Add Stock", command=lambda: [manage_window.destroy(), self.add_stock()]).pack(fill=tk.X, pady=5)
        ttk.Button(manage_window, text="Update Shares", command=lambda: [manage_window.destroy(), self.update_shares_menu()]).pack(fill=tk.X, pady=5)
        ttk.Button(manage_window, text="Delete Stock", command=lambda: [manage_window.destroy(), self.delete_stock()]).pack(fill=tk.X, pady=5)
        ttk.Button(manage_window, text="List Stocks", command=lambda: [manage_window.destroy(), self.list_stocks()]).pack(fill=tk.X, pady=5)
        ttk.Button(manage_window, text="Exit Manage Stocks", command=manage_window.destroy).pack(fill=tk.X, pady=5)

    def add_stock(self):
        symbol = simpledialog.askstring("Input", "Enter Ticker Symbol:", parent=self.root)
        if not symbol:
            return
        symbol = symbol.strip().upper()

        name = simpledialog.askstring("Input", "Enter Company Name:", parent=self.root)
        if not name:
            return
        name = name.strip().upper()

        shares = simpledialog.askfloat("Input", "Enter Number of Shares:", parent=self.root)
        if shares is None:
            return

        try:
            if shares < 0:
                raise ValueError("Shares cannot be negative")
            stock = Stock(symbol, name, shares)
            self.stock_list.append(stock)
            messagebox.showinfo("Success", "Stock Added")
            # Ask if user wants to add another stock
            if messagebox.askyesno("Add Another", "Do you want to add another stock?"):
                self.add_stock()
        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")

    def update_shares_menu(self):
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Shares")
        update_window.geometry("400x200")

        ttk.Label(update_window, text="Update Shares", font=("Arial", 14, "bold")).pack(pady=10)

        ttk.Button(update_window, text="Buy Shares", command=lambda: [update_window.destroy(), self.buy_shares()]).pack(fill=tk.X, pady=5)
        ttk.Button(update_window, text="Sell Shares", command=lambda: [update_window.destroy(), self.sell_shares()]).pack(fill=tk.X, pady=5)
        ttk.Button(update_window, text="Exit Update Shares", command=update_window.destroy).pack(fill=tk.X, pady=5)

    def buy_shares(self):
        if not self.stock_list:
            messagebox.showerror("Error", "No stocks available.")
            return

        stock_symbols = [stock.symbol for stock in self.stock_list]
        symbol = simpledialog.askstring("Input", f"Stock List: {stock_symbols}\nWhich stock do you want to buy?:", parent=self.root)
        if not symbol:
            return
        symbol = symbol.strip().upper()

        for stock in self.stock_list:
            if stock.symbol == symbol:
                shares = simpledialog.askfloat("Input", "How many shares do you want to buy?:", parent=self.root)
                if shares is None:
                    return
                try:
                    if shares <= 0:
                        raise ValueError("Shares must be positive")
                    stock.shares += shares
                    messagebox.showinfo("Success", f"Updated shares for {symbol}: {stock.shares}")
                    return
                except ValueError as e:
                    messagebox.showerror("Error", f"Error: {e}")
                    return
        messagebox.showerror("Error", f"Stock {symbol} not found.")

    def sell_shares(self):
        if not self.stock_list:
            messagebox.showerror("Error", "No stocks available.")
            return

        stock_symbols = [stock.symbol for stock in self.stock_list]
        symbol = simpledialog.askstring("Input", f"Stock List: {stock_symbols}\nWhich stock do you want to sell?:", parent=self.root)
        if not symbol:
            return
        symbol = symbol.strip().upper()

        for stock in self.stock_list:
            if stock.symbol == symbol:
                shares = simpledialog.askfloat("Input", "How many shares do you want to sell?:", parent=self.root)
                if shares is None:
                    return
                try:
                    if shares <= 0:
                        raise ValueError("Shares must be positive")
                    if shares > stock.shares:
                        raise ValueError("Cannot sell more shares than you own")
                    stock.shares -= shares
                    messagebox.showinfo("Success", f"Updated shares for {symbol}: {stock.shares}")
                    return
                except ValueError as e:
                    messagebox.showerror("Error", f"Error: {e}")
                    return
        messagebox.showerror("Error", f"Stock {symbol} not found.")

    def delete_stock(self):
        if not self.stock_list:
            messagebox.showerror("Error", "No stocks available.")
            return

        stock_symbols = [stock.symbol for stock in self.stock_list]
        symbol = simpledialog.askstring("Input", f"Stock List: {stock_symbols}\nWhich stock do you want to delete?:", parent=self.root)
        if not symbol:
            return
        symbol = symbol.strip().upper()

        for i, stock in enumerate(self.stock_list):
            if stock.symbol == symbol:
                self.stock_list.pop(i)
                messagebox.showinfo("Success", f"Stock {symbol} deleted.")
                return
        messagebox.showerror("Error", f"Stock {symbol} not found.")

    def list_stocks(self):
        output = "Stock List ----\n"
        if not self.stock_list:
            output += "No stocks available.\n"
        else:
            output += "SYMBOL\tNAME\t\tSHARES\n"
            for stock in self.stock_list:
                output += f"{stock.symbol}\t{stock.name}\t\t{stock.shares}\n"
        self.display_output(output)

    def add_daily_stock_data(self):
        if not self.stock_list:
            messagebox.showerror("Error", "No stocks available.")
            return

        stock_symbols = [stock.symbol for stock in self.stock_list]
        symbol = simpledialog.askstring("Input", f"Stock List: {stock_symbols}\nWhich stock do you want to use?:", parent=self.root)
        if not symbol:
            return
        symbol = symbol.strip().upper()

        for stock in self.stock_list:
            if stock.symbol == symbol:
                dateFrom = simpledialog.askstring("Input", "Enter starting date (MM/DD/YY):", parent=self.root)
                if not dateFrom:
                    return
                dateTo = simpledialog.askstring("Input", "Enter ending date (MM/DD/YY):", parent=self.root)
                if not dateTo:
                    return

                try:
                    record_count = stock_data.retrieve_stock_web(dateFrom, dateTo, [stock])
                    output = f"\nData fetched for {stock.symbol} ({record_count} records):\n"
                    if stock.daily_data:
                        output += "Date\t\tPrice\t\tVolume\n"
                        for data in stock.daily_data:
                            output += f"{data.date}\t{data.closing_price}\t{data.volume}\n"
                    else:
                        output += "No data retrieved.\n"
                    self.display_output(output)
                    return
                except Exception as e:
                    messagebox.showerror("Error", f"Error fetching data: {str(e)}")
                    return
        messagebox.showerror("Error", f"Stock {symbol} not found.")

    def show_report(self):
        output = "Stock Report ----\n"
        if not self.stock_list:
            output += "No stocks available.\n"
        else:
            for stock in self.stock_list:
                output += f"Report for: {stock.symbol} {stock.name}\n"
                output += f"Shares: {stock.shares}\n"
                if not stock.daily_data:
                    output += "*** No daily history.\n"
                else:
                    for data in stock.daily_data:
                        output += f"Date: {data.date}, Price: {data.closing_price}, Volume: {data.volume}\n"
        self.display_output(output)

    def show_chart(self):
        if not self.stock_list:
            messagebox.showerror("Error", "No stocks available.")
            return

        stock_symbols = [stock.symbol for stock in self.stock_list]
        symbol = simpledialog.askstring("Input", f"Stock List: {stock_symbols}\nWhich stock do you want to use?:", parent=self.root)
        if not symbol:
            return
        symbol = symbol.strip().upper()

        for stock in self.stock_list:
            if stock.symbol == symbol:
                if not stock.daily_data:
                    messagebox.showerror("Error", "No daily data available to plot.")
                    return
                dates = []
                prices = []
                for data in stock.daily_data:
                    try:
                        date = datetime.strptime(data.date, "%m/%d/%y")
                        dates.append(date)
                        prices.append(data.closing_price)
                    except ValueError as e:
                        messagebox.showerror("Error", f"Error parsing date {data.date}: {e}. Skipping this entry.")
                        continue
                
                if not dates:
                    messagebox.showerror("Error", "No valid data to plot.")
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
        messagebox.showerror("Error", f"Stock {symbol} not found.")

    def manage_data_menu(self):
        manage_data_window = tk.Toplevel(self.root)
        manage_data_window.title("Manage Data")
        manage_data_window.geometry("400x300")

        ttk.Label(manage_data_window, text="Manage Data", font=("Arial", 14, "bold")).pack(pady=10)

        ttk.Button(manage_data_window, text="Save Data to Database", command=lambda: [manage_data_window.destroy(), self.save_to_database()]).pack(fill=tk.X, pady=5)
        ttk.Button(manage_data_window, text="Load Data from Database", command=lambda: [manage_data_window.destroy(), self.load_from_database()]).pack(fill=tk.X, pady=5)
        ttk.Button(manage_data_window, text="Retrieve Data from Web", command=lambda: [manage_data_window.destroy(), self.retrieve_from_web()]).pack(fill=tk.X, pady=5)
        ttk.Button(manage_data_window, text="Import from CSV File", command=lambda: [manage_data_window.destroy(), self.import_csv()]).pack(fill=tk.X, pady=5)
        ttk.Button(manage_data_window, text="Exit Manage Data", command=manage_data_window.destroy).pack(fill=tk.X, pady=5)

    def save_to_database(self):
        dateFrom = "01/01/25"
        dateTo = "12/31/25"
        try:
            stock_data.retrieve_stock_web(dateFrom, dateTo, self.stock_list)
            temp_filename = "temp_stock_data.csv"
            with open(temp_filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Symbol", "Date", "Price", "Volume"])
                for stock in self.stock_list:
                    for data in stock.daily_data:
                        writer.writerow([stock.symbol, data.date, data.closing_price, data.volume])
            
            filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Save Stock Data As")
            if filename:
                import shutil
                shutil.move(temp_filename, filename)
                messagebox.showinfo("Success", f"Data saved to {filename}")
            else:
                messagebox.showinfo("Info", "No filename provided, data saved as temp_stock_data.csv")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving data: {str(e)}")

    def load_from_database(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")], title="Load Stock Data")
        if not filename:
            return

        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                symbol = simpledialog.askstring("Input", "Enter stock symbol to load:", parent=self.root)
                if not symbol:
                    return
                symbol = symbol.strip().upper()

                dateFrom = simpledialog.askstring("Input", "Enter starting date (MM/DD/YY):", parent=self.root)
                if not dateFrom:
                    return
                dateTo = simpledialog.askstring("Input", "Enter ending date (MM/DD/YY):", parent=self.root)
                if not dateTo:
                    return

                start_date = datetime.strptime(dateFrom, "%m/%d/%y")
                end_date = datetime.strptime(dateTo, "%m/%d/%y")
                for stock in self.stock_list:
                    if stock.symbol == symbol:
                        stock.daily_data = []
                        for row in reader:
                            if row[0] == symbol:
                                row_date = datetime.strptime(row[1], "%m/%d/%y")
                                if start_date <= row_date <= end_date:
                                    daily_data = DailyData(row[1], float(row[2]), int(row[3]))
                                    stock.add_daily_data(daily_data)
                        output = f"\nData loaded for {symbol} within {dateFrom} to {dateTo}:\n"
                        if stock.daily_data:
                            output += "Date\t\tPrice\t\tVolume\n"
                            for data in stock.daily_data:
                                output += f"{data.date}\t{data.closing_price}\t{data.volume}\n"
                        else:
                            output += "No data found for the specified date range.\n"
                        self.display_output(output)
                        break
                else:
                    messagebox.showerror("Error", f"Stock {symbol} not found in portfolio")
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {str(e)}")

    def retrieve_from_web(self):
        dateFrom = simpledialog.askstring("Input", "Enter starting date (MM/DD/YY):", parent=self.root)
        if not dateFrom:
            return
        dateTo = simpledialog.askstring("Input", "Enter ending date (MM/DD/YY):", parent=self.root)
        if not dateTo:
            return

        try:
            record_count = stock_data.retrieve_stock_web(dateFrom, dateTo, self.stock_list)
            self.display_output(f"Records Retrieved: {record_count}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error retrieving data: {str(e)}")

    def import_csv(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")], title="Import Stock Data")
        if not filename:
            return

        if not self.stock_list:
            messagebox.showerror("Error", "No stocks available.")
            return

        stock_symbols = [stock.symbol for stock in self.stock_list]
        symbol = simpledialog.askstring("Input", f"Stock List: {stock_symbols}\nWhich stock do you want to use?:", parent=self.root)
        if not symbol:
            return
        symbol = symbol.strip().upper()

        try:
            for stock in self.stock_list:
                if stock.symbol == symbol:
                    stock.daily_data = []
                    if stock_data.import_stock_web_csv(self.stock_list, symbol, filename):
                        output = "CSV File Imported\n"
                        output += f"\nData imported for {symbol}:\n"
                        if stock.daily_data:
                            output += "Date\t\tPrice\t\tVolume\n"
                            for data in stock.daily_data:
                                output += f"{data.date}\t{data.closing_price}\t{data.volume}\n"
                        else:
                            output += "No data imported.\n"
                        self.display_output(output)
                    else:
                        messagebox.showerror("Error", f"Stock {symbol} not found in portfolio")
                    break
        except Exception as e:
            messagebox.showerror("Error", f"Error importing CSV: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StockGUI(root)
    root.mainloop()