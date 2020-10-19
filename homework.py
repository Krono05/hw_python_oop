import datetime as dt
date_format = "%d.%m.%Y"


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):

        today = dt.date.today()
        return sum(
            record.amount
            for record in self.records
            if record.date == today
        )

    def get_week_stats(self):

        today_date = dt.date.today()
        seven_days = dt.timedelta(days=7)
        week_ago = today_date - seven_days
        return sum(
            record.amount
            for record in self.records
            if week_ago <= record.date <= today_date)


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, date_format).date()


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        today_stock_calories = self.limit - self.get_today_stats()
        if today_stock_calories > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью '
                    f'не более {today_stock_calories} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):

    USD_RATE = 77.50
    EURO_RATE = 91.00

    def get_today_cash_remained(self, currency):
        currencies = {
            'rub': (1, 'руб'),
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro')
        }
        if currency not in currencies:
            return f'Валюта не поддерживается'
        rate, symbol = currencies[currency]
        balance = self.limit - self.get_today_stats()
        if balance == 0:
            return f'Денег нет, держись'
        if balance < 0:
            balance = abs(balance)
            return (f'Денег нет, держись: твой долг - '
                    f'{(balance/rate):.2f} {symbol}')
        return (f'На сегодня осталось {(balance/rate):.2f} {symbol}')


if __name__ == "__main__":
    cash_calculator = CashCalculator(1200)
    cash_calculator.add_record(Record(amount=200, comment="кофе"))
    cash_calculator.add_record(Record(amount=800, comment="Серёге за обед"))
    cash_calculator.add_record(Record(
                                amount=300, comment="бар в Танин др",
                                date="08.11.2019"))
    print(cash_calculator.get_today_cash_remained("rub"))
    print(cash_calculator.get_today_cash_remained("usd"))
    print(cash_calculator.get_week_stats())

    calories_calculator = CaloriesCalculator(1000)
    calories_calculator.add_record(Record(amount=500, comment="кофе"))
    calories_calculator.add_record(Record(amount=400, comment="кофе"))
    calories_calculator.add_record(Record(
                                    amount=300, comment="бар в Танин др",
                                    date="08.11.2019"))
    print(calories_calculator.get_calories_remained())
    print(calories_calculator.get_week_stats())
