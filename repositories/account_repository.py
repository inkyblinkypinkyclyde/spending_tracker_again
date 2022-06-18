from db.run_sql import run_sql

from models.account import Account

def save(account):
    sql = 'INSERT INTO accounts (name, description, balance) VALUES (%s, %s, %s) RETURNING *'
    values = [account.name, account.description, account.balance]
    results = run_sql(sql, values)
    id = results[0]['id']
    account.id = id
    return account

def select_all():
    accounts = []
    sql = "SELECT * FROM accounts"
    results = run_sql(sql)
    for row in results:
        account = Account(row['name'], row['description'], row['balance'], row['id'])
        accounts.append(account)
    return accounts


def select(id):
    account = None
    sql = "SELECT * FROM accounts WHERE id = %s"
    values = [id]
    result = run_sql(sql, values)[0]

    if result is not None:
        account = Account(result['name'], result['description'], result['balance'], result['id'])
    return account

def delete_all():
    sql = 'DELETE FROM accounts'
    run_sql(sql)

def delete(id):
    sql = 'DELETE FROM accounts WHERE id = %s'
    values = [id]
    run_sql(sql, values)

def update(account):
    sql = 'UPDATE accounts SET (name, description, balance) = (%s, %s, %s) WHERE id = %s'
    values = [account.name, account.description, account.balance, account.id]
    run_sql(sql, values)