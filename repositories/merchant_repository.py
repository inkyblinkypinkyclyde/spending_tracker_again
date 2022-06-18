from db.run_sql import run_sql

from models.merchant import Merchant

def save(merchant):
    sql = 'INSERT INTO merchants (name, balance, description) VALUES (%s, %s, %s) RETURNING *'
    values = [merchant.name, merchant.balance, merchant.description]
    results = run_sql(sql, values)
    id = results[0]['id']
    merchant.id = id
    return merchant

def select_all():
    merchants = []
    sql = "SELECT * FROM merchants"
    results = run_sql(sql)
    for row in results:
        merchant = Merchant(row['name'], row['balance'], row['description'], row['id'])
        merchants.append(merchant)
    return merchants


def select(id):
    merchant = None
    sql = "SELECT * FROM merchants WHERE id = %s"
    values = [id]
    result = run_sql(sql, values)[0]
    if result is not None:
        merchant = Merchant(result['name'], result['balance'], result['description'], result['id'])
    return merchant

def delete_all():
    sql = 'DELETE FROM merchants'
    run_sql(sql)

def delete(id):
    sql = 'DELETE FROM merchants WHERE id = %s'
    values = [id]
    run_sql(sql, values)

def update(merchant):
    sql = 'UPDATE merchants SET (name, balance, description) = (%s, %s, %s) WHERE id = %s'
    values = [merchant.name, merchant.balance, merchant.description, merchant.id]
    # breakpoint()
    run_sql(sql, values)

def find_merchant_by_name(name):
    for merchant in select_all():
        if merchant.name == name:
            return merchant
