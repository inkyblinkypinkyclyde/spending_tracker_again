from flask import Flask, render_template, redirect, Blueprint, request, url_for
from controllers.transactions_controller import transactions
from models.account import Account
from models.transaction import Transaction
import repositories.account_repository as account_repository
import repositories.transaction_repository as transaction_repository
import repositories.merchant_repository as merchant_repository
from datetime import *

accounts_blueprint = Blueprint("accounts", __name__)

@accounts_blueprint.route("/accounts")
def accounts():
    accounts = account_repository.select_all()
    for account in accounts:
        account.balance = transaction_repository.get_all_balances_today(account.id)
    return render_template("accounts/index.html", all_accounts = accounts)

@accounts_blueprint.route("/accounts/new", methods=['GET'])
def new_account():
    accounts = account_repository.select_all()
    for account in accounts:
        account.balance = transaction_repository.get_all_balances_today(account.id)
    return render_template("accounts/new.html", all_accounts = accounts)

@accounts_blueprint.route("/accounts", methods=['POST'])
def create_account():
    name = request.form['name']
    description = request.form['description']
    balance = request.form['balance']
    account = Account(name, description, balance)
    account_repository.save(account)
    return redirect('/accounts')

@accounts_blueprint.route("/accounts/<id>/edit", methods=['GET'])
def edit_account(id):
    accounts = account_repository.select_all()
    for account in accounts:
        account.balance = transaction_repository.get_all_balances_today(account.id)
    account = account_repository.select(id)
    return render_template('accounts/edit.html', account = account, all_accounts = accounts)

@accounts_blueprint.route("/accounts/<id>", methods=['POST'])
def update_account(id):
    name = request.form['name']
    description = request.form['description']
    balance = request.form['balance']
    account = Account(name, description, balance, id)
    account_repository.update(account)
    return redirect('/accounts')

@accounts_blueprint.route("/accounts/<id>/delete", methods=['GET'])
def delete_account_check(id):
    accounts = account_repository.select_all()
    for account in accounts:
        account.balance = transaction_repository.get_all_balances_today(account.id)
    account = account_repository.select(id)
    return render_template('/accounts/delete.html', account = account, all_accounts = accounts)

@accounts_blueprint.route("/accounts/<id>/delete-account", methods=["POST"])
def delete_account(id):
    account_repository.delete(id)
    return redirect('/accounts')

@accounts_blueprint.route("/future")
def accounts_by_day():
    accounts = account_repository.select_all()
    transactions = transaction_repository.select_all()
    for account in accounts:
        account.balance = transaction_repository.get_all_balances_today(account.id)
    if request.args:
        accounts_for_future = account_repository.select_all()
        date = request.args['date']
        transactions_for_future = transaction_repository.select_all_before_date(date)
        for account in accounts_for_future:
            account.balance = transaction_repository.get_any_balance_by_date(account.id, date)
        return render_template(
        '/future.html',
        all_accounts = accounts,
        all_accounts_for_future = accounts_for_future,
        all_transactions = transactions,
        all_transactions_for_future = transactions_for_future,
        date = date
        )
    return render_template('/future.html', all_accounts = accounts, all_transactions = transactions)

@accounts_blueprint.route("/future", methods=["POST"])
def make_transfer():
    amount_out = f"{float(request.form['amount'])*100:.0f}"
    date = request.form['date']
    email = request.form['email']
    description = 'transfer'
    merchant = merchant_repository.find_merchant_by_name('transaction_holder')
    account_id_out = request.form['account_id_out']
    account_out = account_repository.select(account_id_out)
    transaction_out = Transaction(amount_out, date, description, account_out, merchant)
    transaction_repository.save(transaction_out)
    account_id_in = request.form['account_id_in']
    account_in = account_repository.select(account_id_in)
    transaction_in = Transaction(str(-abs(int(amount_out))), date, description, account_in, merchant)
    transaction_repository.save(transaction_in)
    if email == 'True':
        return redirect(url_for('send_mail', account1 = account_out.name, account2 = account_in.name, amount = amount_out, date = date))
    return redirect('/accounts')