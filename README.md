# StockAnalyzer

# Stock Analyzer Application

## Description

The Stock Analyzer is a Python-based application designed to help users manage a stock portfolio, retrieve historical stock data, generate analytical reports, create visual charts, and handle data import/export via CSV files. The application offers both a console-based interface (CLI) and a graphical user interface (GUI).

This project allows users to track stock performance, make informed decisions based on historical data, and manage their portfolio information efficiently. Data is primarily fetched from Yahoo! Finance and can be saved/loaded locally using CSV files.

## Features

The application provides the following key features through both Console and GUI versions:

* **Portfolio Management:**
    * Add new stocks to the portfolio.
    * Update existing stock details (e.g., number of shares through buy/sell operations).
    * Delete stocks from the portfolio.
    * List all stocks currently in the portfolio with their details.
* **Historical Data Retrieval:**
    * Fetch historical daily stock data (date, price, volume) for specific stocks from Yahoo! Finance over a defined date range.
* **Reporting:**
    * Generate and display a consolidated report showing all stocks in the portfolio along with their daily historical data.
* **Charting:**
    * Visualize the price history of a selected stock by generating a line chart using Matplotlib.
* **Data Management (using CSV files):**
    * **Save Portfolio Data:** Save the current portfolio's stock data (including daily history) to a CSV file.
    * **Load Portfolio Data:** Load previously saved stock data from a CSV file.
    * **Retrieve Data from Web:** Fetch historical data from Yahoo! Finance for all stocks currently in the portfolio list.
    * **Import from CSV:** Import historical data for a specific stock from a Yahoo! Finance formatted CSV file.

## Technologies Used

* **Programming Language:** Python
* **Libraries:**
    * `selenium`: For web scraping (automating browser interaction to fetch data from Yahoo! Finance).
    * `BeautifulSoup4 (bs4)`: For parsing HTML content obtained via web scraping.
    * `matplotlib`: For generating stock price charts.
    * `tkinter`: For the graphical user interface (GUI). (Standard Python library)
* **External Dependencies:**
    * `chromedriver` (or a similar WebDriver for your preferred browser, e.g., GeckoDriver for Firefox): Required by Selenium to control the web browser.

## Project Structure

The project consists of the following key files:

* `stock.py`: Defines the core data models for the application, primarily the `Stock` class (representing an individual stock with attributes like symbol, name, shares, and daily data) and the `DailyData` class (storing date, closing price, and volume).
* `stock_data.py`: Contains modules responsible for data acquisition and importation:
    * `retrieve_stock_web()`: Fetches historical stock data from Yahoo! Finance.
    * `import_stock_web_csv()`: Imports stock data from a downloaded Yahoo! Finance CSV file.
* `stock_console.py`: Implements the console-based user interface (CLI) for interacting with the application.
* `stock_GUI.py`: Implements the graphical user interface (GUI) using Tkinter, providing a visual way to interact with the application.
* `README.md`: This file.

## Setup and Installation

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-name>
    ```

2.  **Install Python:**
    Ensure you have Python 3.x installed on your system.

3.  **Install Dependencies:**
    Install the required Python libraries using pip:
    ```bash
    pip install selenium beautifulsoup4 matplotlib
    ```
    (Tkinter is usually included with Python standard installations.)

4.  **Set up WebDriver:**
    * Download `chromedriver` (if you are using Google Chrome) that matches your Chrome browser version from [https://sites.google.com/a/chromium.org/chromedriver/downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads).
    * Place the `chromedriver` executable in your system's PATH, or directly in the project's root directory.
    * *Note:* If using a different browser, download the appropriate WebDriver (e.g., GeckoDriver for Firefox) and ensure it's in your PATH or project directory. The code in `stock_data.py` might need adjustment if not using Chrome.

## Usage

The application can be run in two modes:

**Console Version, GUI Version**

Navigate to the project directory in your terminal and run:

```bash
python stock_console.py

```bash
python stock_GUI.py
