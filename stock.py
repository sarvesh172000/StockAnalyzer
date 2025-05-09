class DailyData:
    def __init__(self, date, closing_price, volume):
        self.date = date
        self.closing_price = closing_price
        self.volume = volume

class Stock:
    def __init__(self, symbol, name, shares):
        self.symbol = symbol
        self.name = name
        self.shares = shares
        self.daily_data = []

    def add_daily_data(self, daily_data):
        self.daily_data.append(daily_data)