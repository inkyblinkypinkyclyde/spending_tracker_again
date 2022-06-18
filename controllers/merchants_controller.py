from flask import Flask, render_template, redirect, Blueprint, request
from models.merchant import Merchant
import repositories.merchant_repository as merchant_repository
import repositories.account_repository as account_repository
import repositories.transaction_repository as transaction_repository

merchants_blueprint = Blueprint("mechants", __name__)

@merchants_blueprint.route("/merchants")
def merchants():
    merchants = merchant_repository.select_all()
    accounts = account_repository.select_all()
    for account in accounts:
        account.balance = transaction_repository.get_all_balances_today(account.id)
    return render_template("merchants/index.html", all_merchants = merchants, all_accounts = accounts)

@merchants_blueprint.route("/merchants/new", methods=['GET'])
def new_merchant():
    merchants = merchant_repository.select_all()
    accounts = account_repository.select_all()
    for account in accounts:
        account.balance = transaction_repository.get_all_balances_today(account.id)
    return render_template("merchants/new.html", all_merchants = merchants, all_accounts = accounts)

@merchants_blueprint.route("/merchants", methods=['POST'])
def create_merchant():
    name = request.form['name']
    balance = request.form['balance']
    description = request.form['description']
    merchant = Merchant(name, balance, description)
    merchant_repository.save(merchant)
    return redirect('/merchants')

@merchants_blueprint.route("/merchants/<id>/edit", methods=['GET'])
def edit_merchant(id):
    accounts = account_repository.select_all()
    for account in accounts:
        account.balance = transaction_repository.get_all_balances_today(account.id)
    merchant = merchant_repository.select(id)
    return render_template('merchants/edit.html', merchant = merchant, all_accounts = accounts)

@merchants_blueprint.route("/merchants/<id>", methods=['POST'])
def update_merchant(id):
    name = request.form['name']
    description = request.form['description']
    balance = request.form['balance']
    merchant = Merchant(name, description, balance, id)
    merchant_repository.update(merchant)
    return redirect('/merchants')

@merchants_blueprint.route("/merchants/<id>/delete", methods=['GET'])
def delete_merchant_check(id):
    merchant = merchant_repository.select(id)
    accounts = account_repository.select_all()
    for account in accounts:
        account.balance = transaction_repository.get_all_balances_today(account.id)
    return render_template('/merchants/delete.html', merchant = merchant, all_accounts = accounts)

@merchants_blueprint.route("/merchants/<id>/delete-merchant", methods=["POST"])
def delete_merchant(id):
    merchant_repository.delete(id)
    return redirect('/merchants')