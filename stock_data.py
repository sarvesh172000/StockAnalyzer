import time
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
from stock import Stock, DailyData
from datetime import datetime

def retrieve_stock_web(dateStart, dateEnd, stock_list):
    dateFrom = str(int(time.mktime(time.strptime(dateStart, "%m/%d/%y"))))
    dateTo = str(int(time.mktime(time.strptime(dateEnd, "%m/%d/%y"))))
    recordCount = 0

    for stock in stock_list:
        stockSymbol = stock.symbol
        url = f"https://finance.yahoo.com/quote/{stockSymbol}/history?period1={dateFrom}&period2={dateTo}&interval=1d&filter=history&frequency=1d"
        
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.javascript": 2})
        
        try:
            driver = webdriver.Chrome(options=options)
            driver.implicitly_wait(60)
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            driver.quit()
            
            table = soup.find('table')
            if not table:
                continue
                
            dataRows = table.find_all('tr')
            for row in dataRows:
                rowList = [td.text.strip() for td in row.find_all('td')]
                if len(rowList) == 7:
                    try:
                        # Parse the date from Yahoo! Finance format (e.g., "Jan 05, 2025")
                        raw_date = rowList[0]
                        parsed_date = datetime.strptime(raw_date, "%b %d, %Y")
                        # Convert to MM/DD/YY format
                        formatted_date = parsed_date.strftime("%m/%d/%y")
                        daily_data = DailyData(formatted_date, float(rowList[4]), int(rowList[6].replace(',', '')))
                        stock.add_daily_data(daily_data)
                        recordCount += 1
                    except (ValueError, IndexError) as e:
                        print(f"Error parsing row {rowList}: {e}")
                        continue
                        
        except Exception as e:
            driver.quit()
            raise RuntimeError("Chrome Driver Not Found or Error: " + str(e))
            
    return recordCount

def import_stock_web_csv(stock_list, symbol, filename):
    for stock in stock_list:
        if stock.symbol.upper() == symbol.upper():
            with open(filename, 'r') as file:
                data_reader = csv.reader(file, delimiter=',')
                next(data_reader)  # Skip header row
                for row in data_reader:
                    try:
                        daily_data = DailyData(row[0], float(row[4]), int(row[6].replace(',', '')))
                        stock.add_daily_data(daily_data)
                    except (ValueError, IndexError):
                        continue
            return True
    return False