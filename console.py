from gettext import translation
import pdb
from datetime import date
from models.account import Account
from models.merchant import Merchant
from models.transaction import Transaction
from models.merchant import Merchant

import repositories.account_repository as account_repository
import repositories.transaction_repository as transaction_repository
import repositories.merchant_repository as merchant_repository

transaction_repository.delete_all()
account_repository.delete_all()
merchant_repository.delete_all()

merchant_0 = Merchant("transaction_holder", 0, "You should never see this")
merchant_repository.save(merchant_0)
merchant_0 = Merchant("transaction_holder", 0, "You should never see this", 999)
merchant_repository.update(merchant_0)



account_1 = Account("Halifax", "Current account", 100000)
account_repository.save(account_1)
account_2 = Account("Credit Suisse", "Savings account", 1000000)
account_repository.save(account_2)


merchant_1 = Merchant("A1 Cabs", 0, "taxi company")
merchant_repository.save(merchant_1)
merchant_2 = Merchant("Ryanair", 0, "best budget airline")
merchant_repository.save(merchant_2)
merchant_3 = Merchant("Tesco", 0, "Supermarket")
merchant_repository.save(merchant_3)
merchant_4 = Merchant("Mr. Heckles", 0, "Landlord")
merchant_repository.save(merchant_4)
merchant_5 = Merchant("BT", 0, "Phone and internet supplier")
merchant_repository.save(merchant_5)
merchant_6 = Merchant("British Gas", 0, "Energy supplier")
merchant_repository.save(merchant_6)
merchant_7 = Merchant("Netflix", 0, "entertainment")
merchant_repository.save(merchant_7)
merchant_8 = Merchant("Dominoes", 0, "Pizza emporium")
merchant_repository.save(merchant_8)

transaction_1 = Transaction(50000, "2022-06-01", "Rent", account_1, merchant_4)
transaction_repository.save(transaction_1)
transaction_2 = Transaction(5000, "2022-06-01", "Phone bill", account_1, merchant_5)
transaction_repository.save(transaction_2)
transaction_3 = Transaction(8000, "2022-06-01", "Gas and Electric", account_1, merchant_5)
transaction_repository.save(transaction_3)
transaction_4 = Transaction(1699, "2022-06-10", "entertainment", account_1, merchant_7)
transaction_repository.save(transaction_4)
transaction_5 = Transaction(1250, "2022-06-13", "bought pizza", account_1, merchant_8)
transaction_repository.save(transaction_5)

pdb.set_trace()