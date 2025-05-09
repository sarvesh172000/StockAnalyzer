import csv
from stock import Stock, DailyData
from datetime import datetime
import stock_data

def export_to_csv(stock_list, is_gui=False, root=None):
    dateFrom = "01/01/25"  # Arbitrary start date
    dateTo = "12/31/25"    # Arbitrary end date
    try:
        # Fetch data for all stocks
        stock_data.retrieve_stock_web(dateFrom, dateTo, stock_list)
        temp_filename = "temp_stock_data.csv"
        
        # Write data to temporary CSV file
        with open(temp_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Symbol", "Date", "Price", "Volume"])  # Header
            for stock in stock_list:
                for data in stock.daily_data:
                    writer.writerow([stock.symbol, data.date, data.closing_price, data.volume])
        
        if is_gui:
            # GUI version: Use file dialog to get filename
            import tkinter.filedialog as filedialog
            import tkinter.messagebox as messagebox
            filename = filedialog.asksaveasfilename(
                parent=root,
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Save Stock Data As"
            )
            if filename:
                import shutil
                shutil.move(temp_filename, filename)
                messagebox.showinfo("Success", f"Data saved to {filename}")
            else:
                messagebox.showinfo("Info", "No filename provided, data saved as temp_stock_data.csv")
        else:
            # Console version: Prompt for filename
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
        if is_gui:
            messagebox.showerror("Error", f"Error saving data: {str(e)}")
        else:
            print(f"Error saving data: {str(e)}")
            input("Press Enter to Continue")

def load_from_csv(filename, stock_list, symbol, dateFrom, dateTo, is_gui=False):
    try:
        start_date = datetime.strptime(dateFrom, "%m/%d/%y")
        end_date = datetime.strptime(dateTo, "%m/%d/%y")
        output = f"\nData loaded for {symbol} within {dateFrom} to {dateTo}:\n"
        
        for stock in stock_list:
            if stock.symbol == symbol:
                stock.daily_data = []  # Clear existing data
                with open(filename, 'r') as file:
                    reader = csv.reader(file)
                    next(reader)  # Skip header
                    for row in reader:
                        if row[0] == symbol:  # Match stock symbol
                            row_date = datetime.strptime(row[1], "%m/%d/%y")
                            if start_date <= row_date <= end_date:
                                daily_data = DailyData(row[1], float(row[2]), int(row[3]))
                                stock.add_daily_data(daily_data)
                
                # Prepare output
                if stock.daily_data:
                    output += "Date\t\tPrice\t\tVolume\n"
                    for data in stock.daily_data:
                        output += f"{data.date}\t{data.closing_price}\t{data.volume}\n"
                else:
                    output += "No data found for the specified date range.\n"
                return output, True
        # If stock not found
        if is_gui:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"Stock {symbol} not found in portfolio")
        else:
            print(f"Stock {symbol} not found in portfolio")
        return "", False

    except FileNotFoundError:
        if is_gui:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", "File not found.")
        else:
            print("File not found.")
        return "", False
    except Exception as e:
        if is_gui:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"Error loading data: {str(e)}")
        else:
            print(f"Error loading data: {str(e)}")
        return "", False