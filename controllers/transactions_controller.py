from flask import Flask, redirect, render_template, request, Blueprint

from models.transaction import Transaction

import repositories.transaction_repository as transaction_repository
import repositories.merchant_repository as merchant_repository
import repositories.account_repository as account_repository



transactions_blueprint = Blueprint("transactions", __name__)

@transactions_blueprint.route("/transactions")
def transactions():
    transactions = transaction_repository.select_all()
    accounts = account_repository.select_all()

    for account in accounts:
        account.balance = transaction_repository.get_all_balances_today(account.id)
    return render_template("transactions/index.html", all_transactions = transactions, all_accounts = accounts)

@transactions_blueprint.route("/transactions/new", methods=['GET'])
def new_transaction():
    transactions = transaction_repository.select_all()
    merchants = merchant_repository.select_all()
    accounts = account_repository.select_all()
    for account in accounts:
        account.balance = transaction_repository.get_all_balances_today(account.id)
    return render_template("transactions/new.html", all_transactions = transactions, all_merchants = merchants, all_accounts = accounts)

@transactions_blueprint.route("/transactions", methods=['POST'])
def create_transaction():
    amount = f"{float(request.form['amount'])*100:.0f}"
    date = request.form['date']
    description = request.form['description']
    account_id = request.form['account_id']
    merchant_id = request.form['merchant_id']
    account = account_repository.select(account_id)
    merchant = merchant_repository.select(merchant_id)
    transaction = Transaction(amount, date, description, account, merchant)
    transaction_repository.save(transaction)
    return redirect('/transactions')

@transactions_blueprint.route("/transactions/<id>/edit", methods=['GET'])
def edit_transaction(id):
    transaction = transaction_repository.select(id)
    merchants = merchant_repository.select_all()
    accounts = account_repository.select_all()
    for account in accounts:
        account.balance = transaction_repository.get_all_balances_today(account.id)
    return render_template('transactions/edit.html', transaction = transaction, all_merchants = merchants, all_accounts = accounts)

@transactions_blueprint.route("/transactions/<id>", methods=['POST'])
def update_transaction(id):
    amount = f"{float(request.form['amount'])*100:.0f}"
    date = request.form['date']
    description = request.form['description']
    account_id = request.form['account_id']
    merchant_id = request.form['merchant_id']
    account = account_repository.select(account_id)
    merchant = merchant_repository.select(merchant_id)
    transaction = Transaction(amount, date, description, account, merchant, id)
    transaction_repository.update(transaction)
    return redirect('/transactions')

@transactions_blueprint.route("/transactions/<id>/delete", methods=['GET'])
def delete_transaction_check(id):
    accounts = account_repository.select_all()
    for account in accounts:
        account.balance = transaction_repository.get_all_balances_today(account.id)
    transaction = transaction_repository.select(id)
    return render_template('/transactions/delete.html', transaction = transaction, all_accounts = accounts)

@transactions_blueprint.route("/transactions/<id>/delete-transaction", methods=["POST"])
def delete_transaction(id):
    transaction_repository.delete(id)
    return redirect('/transactions')


