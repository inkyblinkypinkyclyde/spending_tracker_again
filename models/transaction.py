from db.run_sql import run_sql
from datetime import date

class Transaction:
    def __init__(self, amount, date, description, account, merchant, id = None):
        self.amount = amount
        self.date = date
        self.description = description
        self.account = account
        self.merchant = merchant
        self.id = id