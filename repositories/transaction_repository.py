from db.run_sql import run_sql
from datetime import date
from models.merchant import Merchant
from models.account import Account

from models.transaction import Transaction
import repositories.account_repository as account_repository
import repositories.merchant_repository as merchant_repository

def save(transaction):
    sql = "INSERT INTO transactions (amount, date, description, account_id, merchant_id) VALUES (%s, TO_DATE(%s, 'YYYY-MM-DD'), %s, %s, %s) RETURNING *"
    values = [transaction.amount, transaction.date, transaction.description, transaction.account.id, transaction.merchant.id]
    results = run_sql(sql, values)
    id = results[0]['id']
    transaction.id = id
    return transaction

def select_all():
    transactions = []
    sql = "SELECT * FROM transactions"
    results = run_sql(sql)
    for row in results:
        account = account_repository.select(row['account_id'])
        merchant = merchant_repository.select(row['merchant_id'])
        transaction = Transaction(f"{row['amount']/100:.2f}", row['date'], row['description'], account, merchant, row['id'])
        transactions.append(transaction)
    return transactions

def select(id):
    account = None
    sql = "SELECT * FROM transactions WHERE id = %s"
    values = [id]
    result = run_sql(sql, values)[0]
    if result is not None:
        account = account_repository.select(result['account_id'])
        merchant = merchant_repository.select(result['merchant_id'])
        account =Transaction(f"{result['amount']/100:.2f}", result['date'], result['description'], account, merchant, result['id'])
    return account

def delete_all():
    sql = 'DELETE FROM transactions'
    run_sql(sql)

def delete(id):
    sql = 'DELETE FROM transactions WHERE id = %s'
    values = [id]
    run_sql(sql, values)

def update(transaction):
    sql = 'UPDATE transactions SET (amount, date, description, account_id, merchant_id) = (%s, %s, %s, %s, %s) WHERE id = %s'
    values = [transaction.amount, transaction.date, transaction.description, transaction.account.id, transaction.merchant.id, transaction.id]
    run_sql(sql, values)

def get_all_balances_today(account_id):
    balance = 0
    sql1 = "SELECT * FROM transactions WHERE date <= %s"
    values1 = [date.today()]
    results = run_sql(sql1, values1)
    for transactions in results:
        if transactions[4] == account_id:
            balance += transactions[1]
    sql2 = "SELECT * FROM ACCOUNTS WHERE id = %s"
    values2 = [account_id]
    found_account = run_sql(sql2, values2)
    balance_today = found_account[0][3] - balance
    return f"{balance_today/100:.2f}"

def get_any_balance_by_date(account_id, date):
    balance = 0
    sql1 = "SELECT * FROM transactions WHERE date <= %s"
    values1 = [date]
    results = run_sql(sql1, values1)
    for transaction in results:
        if transaction[4] == account_id:
            balance += transaction[1]
    sql2 = "SELECT * FROM ACCOUNTS WHERE id = %s"
    values2 = [account_id]
    found_account = run_sql(sql2, values2)
    balance_today = found_account[0][3] - balance
    return f"{balance_today/100:.2f}"

def select_all_before_date(date):
    transactions = []
    sql = "SELECT * FROM transactions WHERE date <= %s"
    values = [date]
    results = run_sql(sql, values)
    for row in results:
        account = account_repository.select(row['account_id'])
        merchant = merchant_repository.select(row['merchant_id'])
        transaction = Transaction(f"{row['amount']/100:.2f}", row['date'], row['description'], account, merchant, row['id'])
        transactions.append(transaction)
    return transactions

